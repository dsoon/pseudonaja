from . import node
from . import identifier
import pseudonaja.c.PParser as PParser
from pseudonaja.c.PSymbolTable import Variable

import pseudonaja.debug as debug

class Unop(node.Node):

    def __init__(self, op, right, lineno):

        super().__init__(lineno)
        self.__op = PParser.PParser.un_op[op.upper()]
        self.__right = right

    def interpret(self):        
        n = self.__right.interpret()

        if isinstance(n, Variable):
            n = n.value

        if   self.__op == 'not':
            return not n

        else:
            raise SyntaxError(f"Invalid op {self.__op}")

    def __str__(self):
        return f"UnOp: '{self.__op}' '{self.__right}'"

    def __repr__(self):
        return self.__str__()
