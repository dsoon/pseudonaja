from . import node

class Literal(node.Node):

    def __init__(self, val, type, lineno):

        super().__init__(lineno)
        self.__value = val
        self.__type = type

    @property
    def value(self):
        return self.__value

    @property
    def type(self):
        return self.__type

    def interpret(self):
        return self.__value

    def __repr__(self):
        return str(self.__value)

