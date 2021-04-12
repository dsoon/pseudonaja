from . import node  
import pseudonaja.c.PInterpreter as pcint

class QueryCommand(node.Node):
  def __init__(self, cmd, lineno):
    super().__init__(lineno)
    self.__command = cmd

  def interpret(self):
    if self.__command == "symboltable":
        print("Dumping symbol table");
        for n, v in pcint.PInterpreter.symbols.items():
            print(f"name='{n}', value='{v}'")

def type_cast(var_type, value):

    val = None
    #Cast the input to the type of the variable
    try:
        if var_type == "INTEGER":
            val = int(value)

        elif var_type == "REAL":
            val = float(value)

        elif var_type == "CHAR":
            val = value[0]

        elif var_type == "BOOLEAN":
            val = value

        elif var_type == "STRING":
            val = str(value)

        elif var_type == "DATE":
            import datetime
            if "/" in value:
                val = value.split("/")
            elif "-" in value:
                val = value.split("-")
            else:
                raise ValueError(f"Invalid date format {value} use dd/mm/yyyy")

            try:
                val = datetime.datetime(int(val[2]), int(val[1]), int(val[0]))
            except ValueError as e:
                raise ValueError(f"Invalid date {val} - {e}")
        else:
            raise ValueError(f"Invalid data type {val}")

    except ValueError as e:
        raise SyntaxError(e)
    
    return val

class ArgList(node.Node):

    def __init__(self, arg1, arg2=None, lineno=-1):
        super().__init__(lineno)
        self.__args = [arg1]
        if arg2 != None:
            self.__args += [arg2]

    def __iadd__(self, arg):
        #print("Debug: __iadd__ called")
        self.__args = arg.args + self.__args
        return self

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.__args):
            val = self.__args[self.n]
            self.n += 1
            return val
        else:
            raise StopIteration

    def __len__(self):
        return len(self.__args)

    @property
    def args(self):
        return self.__args

    def interpret(self):
        return self.args

