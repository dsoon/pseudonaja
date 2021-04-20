import pseudonaja.debug as debug
import pseudonaja.c.ast.literal as literal

class Symbol:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val):
        self.__name = val

class Variable(Symbol):
    def __init__(self, name, type, value=None):
        super().__init__(name)

        self.__value = value
        self.__type = type

    @property
    ### NEED TO FIX THIS - When Variable is defined, it is assigned a Literal
    def value(self):

        if isinstance(self.__value, literal.Literal):
            return self.__value.value
        else:
            return self.__value
    ##########################################################################

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return self.__str__()

class Constant(Variable):
    def __init__(self, name, type, value=None):
        super().__init__(name, type, value)

class Array(Variable):
    def __init__(self, name, type, s_idx, e_idx):
        super().__init__(name, type, [None] * (e_idx - s_idx + 1))

        self.__s_idx = s_idx
        self.__e_idx = e_idx

    @property
    def start_index(self):
        return self.__s_idx

    @start_index.setter
    def start_index(self, value):
        self.__s_idx = value

    @property
    def end_index(self):
        return self.__e_idx

    @end_index.setter
    def end_index(self, value):
        self.__e_idx = value

    def __getitem__(self, idx):

        #print(f"Array __getitem_ called with index {idx}")

        if isinstance(idx, Variable):
            idx = idx.value

        if idx < self.__s_idx or idx > self.__e_idx:
            raise IndexError(f"Index out of range {self.name} [{idx}]")

        #print("Debug __getitem__ line 69 Symbol.py - value type is", type(self.value))

        return self.value[idx - self.__s_idx]

    def __setitem__(self, idx, value):

        #print(f"type of idx = {type(idx)}")
        #print(f"Array __setitem_ called with index {idx} and value {value}")

        if isinstance(idx, Variable):
            idx = idx.value

        if isinstance(value, Variable):
            value = value.value

        if idx < self.__s_idx or idx > self.__e_idx:
            raise IndexError(f"Index out of range {self.name} [{idx}]")

        if self.type == "INTEGER" and not isinstance(value, int):
            raise ValueError(f"Expecting {self.type} got {type(value)}")

        elif self.type == "STRING" and not isinstance(value, str):
            raise ValueError(f"Expecting {self.type} value got {type(value)}")

        self.value[idx - self.__s_idx] = value

    def __str__(self):
        return f"Array({self.name} {self.__s_idx}, {self.__e_idx}) {self.value}"

    def __repr__(self):
        return self.__str__()

class Function(Symbol):
    def __init__(self, name, params, type, statements):
        super().__init__(name)
        self.__params = params
        self.__type = type
        self.__statements = statements

    @property
    def params(self):
        return self.__params

    @property
    def type(self):
        return self.__type

    @property
    def statements(self):
        return self.__statements

    def __str__(self):
        return f"Function name={self.name}, params={self.params}, type={self.type}, statements={self.statements}"

    def __repr__(self):
        return self.__str__()
        
class Procedure(Symbol):
    def __init__(self, name, params, statements):
        super().__init__(name)

        self.__params = params
        self.__statements = statements

    @property
    def params(self):
        return self.__params

    @property
    def statements(self):
        return self.__statements

    def __str__(self):
        return f"Procedure name={self.name}, params={self.params}, statements={self.statements}"

    def __repr__(self):
        return self.__str__()

import pseudonaja.c.PInterpreter as pcint
class SymbolTable:
    def __init__(self):
        self.__table = {}
        self.keys = None
        self.kidx = -1

    def __setitem__(self, idx, val):
        self.__table [idx] = val

    def __getitem__(self, symbol):
        try:
            if symbol not in self.__table: # Global symbol table

                # Is there a call stack?
                if pcint.PInterpreter.stack and len(pcint.PInterpreter.stack) > 0 and isinstance(pcint.PInterpreter.stack[-1], dict):      
                    return pcint.PInterpreter.stack[-1][symbol]

            else:
                return self.__table [symbol]

        except KeyError as e:
            raise SyntaxError(f"Symbol undefined {e}")

    def __iter__(self):
        self.keys = list(self.__table.keys())
        self.kidx=None
        if self.keys:
            self.kidx=0

        return self

    def __next__(self):
        if self.keys and self.kidx < len(self.keys):
            key = self.keys[self.kidx]
            self.kidx += 1
            return key
        else:
            raise StopIteration

    def items(self):
        return self.__table.items()

    @property
    def table(self):
        return self.__table
