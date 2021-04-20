from pseudonaja.c.PLexer  import PLexer
from pseudonaja.c.PParser import PParser
from pseudonaja.c.PSymbolTable import SymbolTable

import pseudonaja.debug as debug

class UnableToContinue(Exception):
    def __init__(self, *args):
        self.__message = args[[0]]
    
    def __str__(self):
        return self.__message

class PInterpreter:

    symbols = SymbolTable()
    stack   = []

    def __init__(self):

        self.lexer = PLexer()
        self.parser = PParser()


    def repl(self):

        prog = []
        finished = False
        while not finished:
            line = input ("Pseudonaja.c>> ")
            if line != None:
                if line[0] == '.':
                    line = line.strip()
                    if len(line) == 1:
                        if len(prog) > 0:
                            try:
                                prog = "\n".join(prog)
                                self.run(prog)
                                prog = []
                            except Exception as e:
                                print(f"Error while running code {e}")
                        else:
                            print("There is nothing to run")

                    elif line == '.quit':
                        finished = True

                    elif line == '.list':
                        for l in prog:
                            print(l)
                    else:
                        print(f"Unrecognised '.' command {line}")
                else:
                    prog.append(line)

    def run(self, program):
        #try:
        
        tokens = self.lexer.tokenize(program)
        self.parser.parse(tokens)
        self.parser.root.interpret()

        #except SyntaxError as e:
        #    print(f"\nSyntax Error: {e}")

        '''
        except UnableToContinue as e:
            print(f"{e}")

        except TypeError as e:
            print(f"{e}")
            
        except ValueError as e:
            print(f"{e}")

        except AssertionError as e:
            print(f"{e}")
        '''