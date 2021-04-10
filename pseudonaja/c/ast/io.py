from . import node
from . import misc
import pseudonaja.c.PInterpreter as pcint

class Input(node.Node):

    def __init__(self, identifier, lineno):

        #print(f"Debug: Output.__init__ {args}")

        super().__init__(lineno)
        self.__identifier = identifier

    def interpret(self):

        # Check to see if the vriable has been declared
        if self.__identifier in pcint.PInterpreter.symbols:

            # Get the variable from the symbol table
            var = pcint.PInterpreter.symbols[self.__identifier]
            val = input()
            while val == "":
                val = input()

            val = misc.type_cast(var.type, val)

            # Set variable's value to the value returned from input
            var.value = val
        else:
            print(f"Error: symbol '{self.__identifier}' undefined on line {self.lineno}")

class Output(node.Node):

    def __init__(self, args, lineno):

        #print(f"Debug: Output.__init__ {args}")

        super().__init__(lineno)

        self.__args = args

    def interpret(self):

        #print(f"Debug: Output.interpret {self.__args}")

        for arg in self.__args:
            print(arg.interpret(), end=" ")

        print()
