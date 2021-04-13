from . import node
from pseudonaja.c.PSymbolTable import Function, Variable
import pseudonaja.c.PInterpreter as pcint
import pseudonaja.debug as debug


# Function declaration with arguments 
class FunctionDecl(node.Node):

  def __init__(self, name, params, type, statements, lineno):
    super().__init__(lineno)
    self.__name  = name
    self.__params  = params
    self.__type  = type
    self.__statements = statements

  def interpret(self):
    pcint.PInterpreter.symbols[self.__name] = Function(self.__name, self.__type, self.__params, self.__statements)

# Function call
class CallFunction(node.Node):

    def __init__(self, name, arglist, lineno):
        super().__init__(lineno)
        self.__name = name
        self.__arglist = arglist
      
    def interpret(self):

        # Create a stackframe and initialise it with the return variable
        stack_frame = {}

        # Internal functions don't need to be declared.
        if self.__name.lower() in ["div", "mod", "random", "len"]:
            
            arg1 = arg2 = None

            if self.__arglist and len(self.__arglist.args) > 0:
                arg1 = self.__arglist.args[0].value
                if len(self.__arglist.args) > 1:
                    arg2 = self.__arglist.args[1].value

            if isinstance(arg1, Variable):
                arg1 = arg1.value

            if isinstance(arg2, Variable):
                arg2 = arg2.value

            if self.__name.lower() == "div":
                return arg1 // arg2

            elif self.__name.lower() == "mod":
                return arg1 % arg2 

            elif self.__name.lower() == "random":
                from random import randint
                return randint(arg1, arg2) 

            else: # default array len command
                
                array_name = self.__arglist.args[0].name 
                try:
                    array_var = pcint.PInterpreter.symbols[array_name]
                except KeyError:
                    raise SyntaxError(f"Array name '{array_name}' undefined while calling len()")
                return array_var.end_index - array_var.start_index + 1
                
        else: # User defined functions

            func = pcint.PInterpreter.symbols[self.__name]
            if func.params:

                # get name of parameters from func in symbol table
                assert len(self.__arglist) == len(func.params), "length of args not equal to length of parameters"
                idx=0
                for arg in self.__arglist:
                    param = func.params[idx]
                    stack_frame[param.name] = Variable(param.name, param.type, arg.interpret())
                    idx +=1

            # Push stack frame
            pcint.PInterpreter.stack.append(stack_frame)

            # Run the function
            func.statements.interpret()

            debug.dprint(f"CallFunction {self.__name} stack after execution {pcint.PInterpreter.stack}")

            # Pop off the stack frame and extract the return value
            stack_frame = pcint.PInterpreter.stack.pop()

            ret_value = stack_frame["__return__"]


            return ret_value

class Return(node.Node):

    def __init__(self, expr, lineno):
        super().__init__(lineno)
        self.__expr = expr

    def interpret(self):
        return self.__expr.interpret()

    def __str__(self):
        return f"Return.__str__, Return self.__expr = {self.__expr}"

    def __repl__(self):
        return self.__str__()
