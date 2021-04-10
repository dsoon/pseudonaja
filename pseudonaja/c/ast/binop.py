from . import node
from . import identifier
import pseudonaja.c.PParser as PParser

class BinOp(node.Node):

    def __init__(self, left, op, right, lineno):

        #print("BinOp().__init__() : Got here")
        super().__init__(lineno)
        self.__left = left
        self.__op = PParser.PParser.bin_op[op.upper()]
        self.__right = right

    def interpret(self):
        from datetime import datetime, timedelta

        if self.__op.lower() in ['and', 'or'] and (isinstance(self.__left, BinOp) ^ isinstance(self.__right, BinOp)):
            raise TypeError(f"{self.__left} '{self.__op}' '{self.__right}' on line {self.lineno}")

        if not isinstance(self.__left, identifier.Identifier) and isinstance(self.__right, identifier.Identifier) and not isinstance(self.__left, BinOp) and not isinstance(self.__right, BinOp) and self.__left.type != self.__right.type:
            raise TypeError(f"{self.__left.type} {self.__op} {self.__right.type} on line {self.lineno}")

        n1 = self.__left.interpret()
        n2 = self.__right.interpret()

        if   self.__op == '>':
            return n1 > n2

        elif self.__op == '>=':
            return n1 >= n2

        elif self.__op == '<':
            return n1 < n2

        elif self.__op == '<=':
            return n1 <= n2

        elif self.__op == '==':
            return n1 == n2

        elif self.__op == '!=':
            return n1 != n2

        elif self.__op == '+':
            if isinstance(n1, datetime):
                return n1 + timedelta(days = n2)
            else:
                return n1 + n2
        elif self.__op == '-':
            if isinstance(n1, datetime):
                return n1 - timedelta(days = n2)
            else:
                return n1 - n2

        elif self.__op == '*':
            if isinstance(n1, datetime):
                raise TypeError(f"Unsupported operation {self.__op} on {n1} on line {self.lineno}")
            return n1 * n2

        elif self.__op == '/':
            if isinstance(n1, datetime):
                raise TypeError(f"Unsupported operation {self.__op} on {n1} on line {self.lineno}")
            return n1 / n2

        elif self.__op == 'and':
            return n1 and n2

        elif self.__op == 'or':
            return n1 or n2

        else:
            raise SyntaxError(f"Invalid op {self.__op}")

    def __str__(self):
        return f"BinOp: '{self.__left}' '{self.__op}' '{self.__right}'"

    def __repr__(self):
        return self.__str__()
