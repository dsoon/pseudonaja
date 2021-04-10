from . import node
from pseudonaja.c import PInterpreter as pcint
from pseudonaja.c.PSymbolTable import Variable

class Repeat(node.Node):

  def __init__(self, statements, condition, lineno):
    super().__init__(lineno)
    self.__statements = statements
    self.__condition  = condition

  def interpret(self):
    while True:
        self.__statements.interpret()
        if self.__condition.interpret():
            break

class While(node.Node):

  def __init__(self, condition, statements, lineno):
    super().__init__(lineno)
    self.__condition  = condition
    self.__statements = statements

  def interpret(self):
    while self.__condition.interpret():
        self.__statements.interpret()

class For(node.Node):

  def __init__(self, identifier, start, end, step, statements, lineno):
    super().__init__(lineno)
    self.__identifier  = identifier
    self.__start = start
    self.__end = end
    self.__step = step
    self.__statements = statements

  def interpret(self):
    stack_frame ={}
    stack_frame[self.__identifier] = Variable(self.__identifier, "INTEGER")

    # Push stack frame
    pcint.PInterpreter.stack.append(stack_frame)

    step = 1 if self.__step == None else self.__step.interpret()
    for i in range(self.__start.interpret(), self.__end.interpret(), step):

        stack_frame[self.__identifier].value = i

        # Run the procedure
        self.__statements.interpret()

    # Remove stack frame after procedure is complete
    pcint.PInterpreter.stack.pop() 

