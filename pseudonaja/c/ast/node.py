from abc import ABC, abstractmethod

class Node(ABC):
    '''
    This is the base class for all nodes of the Abstract Syntax Tree.
    This ensure that all subclasses implement the interpret() nmethod.
    It also includes an attribute, lineno, that is used to track where
    parts of the pseudocode program lines are parsed. 
    '''

    def __init__(self, lineno=-1):
        self.lineno = lineno

    @abstractmethod
    def interpret(self):
        pass

    @property
    def lineno(self):
        return self.__lineno

    @lineno.setter
    def lineno(self, l):
        self.__lineno = l
