from . import node
from . import function
import pseudonaja.debug as debug
import pseudonaja.c.PInterpreter as pcint

class StatementList(node.Node):
    '''
    A pseudocode program consists of a list of statements
    This is either a single statement, or a statement followed by another statement
    A statement list is built by appending statements to self.__statements
    '''
    def __init__(self, s1, s2):
        self.__statements = [ s1 ]
        if s2:
            self.__statements += s2.statements

    @property
    def statements(self):
        return self.__statements

    def interpret(self):
        for statement in self.statements:

            if isinstance(statement, function.Return):
                val = statement.interpret()

                assert pcint.PInterpreter.stack and len(pcint.PInterpreter.stack) > 0 and isinstance(pcint.PInterpreter.stack[-1], dict), f"Assert Error: Stackframe missing for function call {self.__name}"

                # return the value through the stackframe
                pcint.PInterpreter.stack[-1]["__return__"] = val 

                break 

            else:
                statement.interpret()
