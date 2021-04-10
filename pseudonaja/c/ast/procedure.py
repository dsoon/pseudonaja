from . import node
from pseudonaja.c.PSymbolTable import Variable, Procedure
from pseudonaja.c import PInterpreter as pcint

class CallProcedure(node.Node):

    def __init__(self, name, arglist, lineno):
        super().__init__(lineno)
        self.__name = name
        self.__arglist = arglist
      
    def interpret(self):
        proc = pcint.PInterpreter.symbols[self.__name]
        if proc.params:
            stack_frame = {}
            # get name of parameters from proc in symbol table
            assert len(self.__arglist) == len(proc.params), "length of args not equal to length of parameters"
            idx=0
            for arg in self.__arglist:
                param = proc.params[idx]
                stack_frame[param.name] = Variable(param.name, param.type, arg.interpret())
                idx +=1
            
            # Push stack frame
            pcint.PInterpreter.stack.append(stack_frame)

            # Run the procedure
            proc.statements.interpret()

            # Remove stack frame after procedure is complete
            pcint.PInterpreter.stack.pop() 
            
        else:
            proc.statements.interpret()

class ProcedureDecl(node.Node):

  def __init__(self, name, args, statements, lineno):
    super().__init__(lineno)
    self.__name  = name
    self.__args = args
    self.__statements = statements

  def interpret(self):
    pcint.PInterpreter.symbols[self.__name] = Procedure(self.__name, self.__args, self.__statements)
