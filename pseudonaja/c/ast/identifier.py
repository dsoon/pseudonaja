from . import node
from . import misc
import pseudonaja.c.PInterpreter as pcint
from pseudonaja.c.PSymbolTable import Variable, Array


class Assign(node.Node):
    '''
    Assign an expression to a variable
    '''
    def __init__(self, var, expr, lineno):
        super().__init__(lineno)

        self.__var = var
        self.__expr = expr

    def interpret(self):

        #print("Debug: Assign.interpret()", self.__var)

        if self.__var.name not in pcint.PInterpreter.symbols:
            #print(pcint.PInterpreter.symbols.table)
            raise SyntaxError(f"Symbol '{self.__var.name}' undefined on line {self.lineno}")

        if isinstance(self.__var, ArrayIdentifier):
            name = self.__var.name
            idx  = self.__var.idx
            pcint.PInterpreter.symbols[name][idx] = self.__expr.interpret()

        elif   isinstance(self.__var, Identifier):
            value = self.__expr.interpret()
            var_type = pcint.PInterpreter.symbols[self.__var.name].type
 
            pcint.PInterpreter.symbols[self.__var.name].value = misc.type_cast(var_type, value)
        else:
            raise SyntaxError(f"Assign.interpret: ID type undefined {self.__var}")


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
        return self.interpret()

    def interpret(self):
        return pcint.PInterpreter.symbols[ self.name ].value


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

    def interpret(self):
        pcint.PInterpreter.symbols[self.__name] = Variable(self.__name, self.__type)

class ArrayIdentifierDecl(IdentifierDecl):

    def __init__(self, name, type, start, end, lineno):
        super().__init__(name, type, lineno)
        self.__start_idx = start
        self.__end_idx = end

    def interpret(self):

        __name, __type  = self.name, self.type
        pcint.PInterpreter.symbols[__name] = Array(__name, __type, self.__start_idx, self.__end_idx)
