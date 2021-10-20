from . import node
from . import misc
import pseudonaja.c.PInterpreter as pcint
from pseudonaja.c.PSymbolTable import Variable, Array, Constant
from pseudonaja.c.ast.literal import Literal

import pseudonaja.debug as debug

class Assign(node.Node):
    '''
    Assign an expression to a variable
    '''
    def __init__(self, var, expr, lineno):
        super().__init__(lineno)

        self.__var = var
        self.__expr = expr

    def interpret(self):

        onstack = False
        if self.__var.name not in pcint.PInterpreter.symbols:

            # check if there is a stackframe
            if pcint.PInterpreter.stack and len(pcint.PInterpreter.stack) > 0 and isinstance(pcint.PInterpreter.stack[-1], dict):

                if self.__var.name not in pcint.PInterpreter.stack[-1]:

                    raise SyntaxError(f"Symbol '{self.__var.name}' undefined on line {self.lineno}")

                else:
                    onstack = True
            else:
                    raise SyntaxError(f"Symbol '{self.__var.name}' undefined on line {self.lineno}")

        if isinstance(self.__var, ArrayIdentifier):

            name = self.__var.name
            idx  = self.__var.idx

            assert name and idx, f"Assertion failed: Array assignment error: {name}[{idx}]" 

            if not onstack:
                pcint.PInterpreter.symbols[name][idx] = self.__expr.interpret()
            else:
                pcint.PInterpreter.stack[-1][name][idx] = self.__expr.interpret()

        elif   isinstance(self.__var, Identifier):
            value = self.__expr.interpret()
            if not onstack:
                if isinstance(pcint.PInterpreter.symbols[self.__var.name], Constant):
                    raise SyntaxError(f"Cannot re-assign constant '{self.__var.name}'")


                # check static typing
                invalid_type = False
                var_type = pcint.PInterpreter.symbols[self.__var.name].type                
                if var_type == "INTEGER":
                    if not isinstance(value, int) or str(value).upper() in ["TRUE", "FALSE"]: # isinstance(True, int) -> True :/ thanks python
                        invalid_type = True

                elif var_type == "REAL":
                    if not isinstance(value, float):
                        invalid_type = True

                elif var_type == "BOOLEAN":
                    if not isinstance(value, bool):
                        invalid_type = True

                # rest are string based
                elif isinstance(value, str):
                    if var_type == "CHAR":
                        if len(value) > 1:
                            invalid_type = True
                    
                    elif var_type == "DATE":
                        import re
                        if not re.match(r'[0-3]?[0-9]/[0-1]?[0-9]/[0-9]{4}', value):
                            invalid_type = True
                else:
                    invalid_type = True
                
                
                
                if invalid_type:
                    raise ValueError(f"Line {self.lineno} variable '{self.__var.name}' must be of type {var_type}")
                    
                pcint.PInterpreter.symbols[self.__var.name].value = misc.type_cast(var_type, value)
            else:
                var_type = pcint.PInterpreter.stack[-1][self.__var.name].type
                pcint.PInterpreter.stack[-1][self.__var.name].value = misc.type_cast(var_type, value)
        else:
            raise SyntaxError(f"Unknown Identifier Type {self.__var}")


class Declare(node.Node):

    def __init__(self, decl, lineno):

            super().__init__(lineno)
            self.__declaration = decl

    def interpret(self):
        self.__declaration.interpret()

    def __str__(self):
        return f"Declare: '{self.__declaration}'"

    def __repr__(self):
        return self.__str__()


class Identifier(node.Node):

    def __init__(self, name, lineno):
        super().__init__(lineno)
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        pcint.PInterpreter.symbols[ self.name ].type

    @property
    def value(self):
        val = self.interpret()
        if isinstance(val, Variable):
            val = val.value
        return val

    def interpret(self):
 
        # check if identifier in the global symbol table
        if self.name not in pcint.PInterpreter.symbols:

            # check if there is a stack frame, if so check if name is in the stack frame
            if len(pcint.PInterpreter.stack) == 0 or isinstance(pcint.PInterpreter.stack[-1], dict) and self.name not in pcint.PInterpreter.stack[-1]: 

                raise SyntaxError(f"Identifier '{self.name}' is undefined")

            else: # found identifier in stack frame
                value = pcint.PInterpreter.stack[-1][self.name]

        else:
            value = pcint.PInterpreter.symbols[ self.name ].value

        return value


class ArrayIdentifier(Identifier):

    def __init__(self, name, expr, lineno):
        super().__init__(name, lineno)
        self.__expr = expr

    @property
    def name(self):
        return super().name

    @property
    def idx(self):
        return self.__expr.interpret()

    def interpret(self):
        return pcint.PInterpreter.symbols[ self.name ] [self.idx]

    def __str__(self):
        return f"ArrayIdentifier {super().name}[ {self.__expr.interpret()} ]"

    def __repr__(self):
        return self.__str__()


class IdentifierDecl(node.Node):

    def __init__(self, name, id_type, lineno):
        super().__init__(lineno)
        self.__name = name
        self.__type = id_type

    @property
    def name(self):
        return self.__name
    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    def interpret(self):
        # check if there is a stack frame (declaration called within a blockstatement)
        if pcint.PInterpreter.stack and len(pcint.PInterpreter.stack) > 0 and isinstance(pcint.PInterpreter.stack[-1], dict):

            # found a stack frame, add variable to stack frame
            pcint.PInterpreter.stack[-1][self.__name] = Variable(self.__name, self.__type) 

        else: # Add to global symbol table
            pcint.PInterpreter.symbols[self.__name] = Variable(self.__name, self.__type)

class ArrayIdentifierDecl(IdentifierDecl):

    def __init__(self, name, type, start, end, lineno):
        super().__init__(name, type, lineno)
        self.__start_idx = start
        self.__end_idx = end

    def interpret(self):

        __name, __type  = self.name, self.type

        # check if there is a stack frame (declaration called within a blockstatement)
        if pcint.PInterpreter.stack and len(pcint.PInterpreter.stack) > 0 and isinstance(pcint.PInterpreter.stack[-1], dict):
            # found a stack frame, add variable to stack frame
            pcint.PInterpreter.stack[-1][__name] = Array(__name, __type, self.__start_idx, self.__end_idx)
 
        else: # Add to global symbol table
            pcint.PInterpreter.symbols[__name] = Array(__name, __type, self.__start_idx, self.__end_idx)

class ConstantDecl(IdentifierDecl): 

    def __init__(self, name, value, lineno):
        super().__init__(name, None, lineno)

        if isinstance(value, Literal):
            self.__value = value.value
        else:
            self.__value = value

    def interpret(self):

        __name = self.name

        if isinstance(self.__value, int):
            self.type = "INTEGER"

        elif isinstance(self.__value, float):
            self.type = "REAL"

        elif isinstance(self.__value, str):

            if len(self.__value) == 1:
                self.type = "CHAR"
            else:
                import re, datetime

                isdate = re.match(r'[0-3]?[0-9]/[0-1]?[0-9]/[0-9]{4}', self.__value)
                if isdate:
                    dd, mm, yyyy = isdate.group().split("/")
                    self.__value = datetime.datetime(int(yyyy), int(mm), int(dd))
                    self.type = "DATE"
                else:
                    self.type = "STRING"

        elif isinstance(self.__value, bool):
            self.type = "BOOLEAN"

        else:
            raise SyntaxError(f"Invalid constant type '{__name}' = {type(self.__value)}")

        # check if there is a stack frame (declaration called within a blockstatement)
        if pcint.PInterpreter.stack and len(pcint.PInterpreter.stack) > 0 and isinstance(pcint.PInterpreter.stack[-1], dict):
            # found a stack frame, add variable to stack frame
            if __name in pcint.PInterpreter.stack[-1]:
                raise SyntaxError(f"Constant {__name} already defined, line {self.lineno}")
            else:
                pcint.PInterpreter.stack[-1][__name] = Constant(__name, self.type, self.__value)

        else: # Add to global symbol table
            if __name in pcint.PInterpreter.symbols:
                raise SyntaxError(f"Constant {__name} already defined, line {self.lineno}")
            else:
                pcint.PInterpreter.symbols[__name] = Constant(__name, self.type, self.__value)
