from . import node
import pseudonaja.debug as debug

class IfThen(node.Node):

  def __init__(self, condition, statements, lineno):
    super().__init__(lineno)
    self.__condition  = condition
    self.__statements = statements

  def interpret(self):

    condition = self.__condition.interpret()

    if condition == True:
        self.__statements.interpret()

class IfThenElse(node.Node):

  def __init__(self, condition, statements1, statements2, lineno):
    super().__init__(lineno)
    self.__condition  = condition
    self.__statements1 = statements1
    self.__statements2 = statements2

  def interpret(self):
    if self.__condition.interpret():
        self.__statements1.interpret()
    else:
        self.__statements2.interpret()

class Case(node.Node):

    def __init__(self, expr, case_list, lineno):
        super().__init__(lineno)
        self.__expr = expr
        self.__case_list = case_list

    def interpret(self):
        expr_val = self.__expr.interpret()
        found, otherwise = False, -1
        for i, c in enumerate(self.__case_list):
            literal, statements = c
            if literal == 'OTHERWISE':
                otherwise = i
            if expr_val == literal:
                statements.interpret()
                found = True
                break
        if not found and otherwise != -1:
            self.__case_list[otherwise][1].interpret()

