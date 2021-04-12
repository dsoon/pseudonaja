from sly import Parser
from pseudonaja.c.ast import identifier as identifier
from pseudonaja.c.ast import misc as misc
from pseudonaja.c.ast import literal as literal
from pseudonaja.c.ast import io as io
from pseudonaja.c.ast import binop as binop
from pseudonaja.c.ast import statement_list as statement_list
from pseudonaja.c.ast import selection as selection
from pseudonaja.c.ast import iteration as iteration
from pseudonaja.c.ast import procedure as procedure
from pseudonaja.c.ast import function as function

from pseudonaja.c import PLexer as PLexer


class PParser(Parser):

    root = None
    tokens = PLexer.PLexer.tokens

    # Un-comment the following line to output the parser logs for debugging any conflicts
    #debugfile = 'parser.out'

    # This sets the order of execution. The last values will have a higher precedence
    precedence = (
        ('right', ASSIGN  ),
        ('left',  OR      ),
        ('left',  AND     ),
        ('left',  EQUAL, NOTEQUAL),
        ('left',  BIGGER, SMALLER),
        ('left',  '+', '-'),
        ('left',  '*', '/'),
        ('right', UMINUS),
        ('left',  '.'     ), # We want to compute the float before do any operation

    )

    @_('statement_list')
    def program(self, p):
        self.root = p[0]

    @_('statement')
    def statement_list(self, p):
        return statement_list.StatementList(p[0], None)

    @_('statement statement_list')
    def statement_list(self, p):
        return statement_list.StatementList(p[0], p[1])

    @_('')
    def empty(self, p):
        pass

    @_('IDENTIFIER ":" TYPE')
    def identifier_type(self, p):
        return identifier.IdentifierDecl(p[0], p[2], p.lineno)

    @_('IDENTIFIER ":" ARRAY "[" NUMBER ":"  NUMBER "]" OF TYPE')
    def identifier_type(self, p):
        return identifier.ArrayIdentifierDecl(p[0], p[9], p[4], p[6], p.lineno)

    @_('identifier_type')
    def identifier_type_list(self, p):
        return [p[0]]

    @_('identifier_type "," identifier_type_list')
    def identifier_type_list(self, p):
        return [p[0]] + p[2]

    @_('empty')
    def identifier_type_list(self, p):
        pass

    # Definitions for statements start here -----------------------------------------------
    @_('DECLARE identifier_type')
    def statement(self, p):
        return identifier.Declare(p[1], p.lineno)

    # Declaring a procedure with 1 or more arguments
    @_('PROCEDURE IDENTIFIER "(" identifier_type_list ")" statement_list ENDPROCEDURE')
    def statement(self, p):
        return procedure.ProcedureDecl(p[1], p[3], p[5], p.lineno)

    # Declaring a procedure w/o arguments
    @_('PROCEDURE IDENTIFIER statement_list ENDPROCEDURE')
    def statement(self, p):
        return procedure.ProcedureDecl(p[1], None, p[2], p.lineno)

    # Declaring a function with 1 or more arguments
    @_('FUNCTION IDENTIFIER "(" identifier_type_list ")" RETURNS TYPE statement_list ENDFUNCTION')
    def statement(self, p):
        return function.FunctionDecl(p[1], p[6], p[3], p[7], p.lineno)

    # Declaring a function with zero arguments
    @_('FUNCTION IDENTIFIER RETURNS TYPE statement_list ENDFUNCTION')
    def statement(self, p):
        return function.FunctionDecl(p[1], p[3], None, p[4], p.lineno)

    # Declaring a procedure w/o arguments
    @_('CALL IDENTIFIER "(" arg_list ")"')
    def statement(self, p):
        return procedure.CallProcedure(p[1], p[3], p.lineno)

    # Declaring a procedure w/o arguments
    @_('CALL IDENTIFIER')
    def statement(self, p):
        return procedure.CallProcedure(p[1], None, p.lineno)

    @_('variable ASSIGN expression')
    def statement(self, p):
        return identifier.Assign(p[0], p[2], p.lineno)

    @_('INPUT IDENTIFIER')
    def statement(self, p):
        return io.Input(p[1],p.lineno)

    @_('OUTPUT arg_list')
    def statement(self, p):
        return io.Output(p[1], p.lineno)

    @_('IF expression THEN statement_list ENDIF')
    def statement(self, p):
        return selection.IfThen(p[1], p[3], p.lineno)

    @_('IF expression THEN statement_list ELSE statement_list ENDIF')
    def statement(self, p):
        return selection.IfThenElse(p[1], p[3], p[5], p.lineno)

    @_('CASE OF expression caselist ENDCASE')
    def statement(self, p):
        return selection.Case(p[2], p[3], p.lineno)

    @_('a_case')
    def caselist(self, p):
        return [p[0]]

    @_('a_case caselist')
    def caselist(self, p):
        return [p[0] ] + p[1]

    @_('constant ":" statement', 'OTHERWISE ":" statement')
    def a_case(self, p):
        return (p[0], p[2])

    @_('STRING', 'NUMBER')
    def constant(self, p):
        return p[0]

    @_('WHILE expression DO statement_list ENDWHILE')
    def statement(self, p):
        return iteration.While( p[1], p[3], p.lineno)

    @_('REPEAT statement_list UNTIL expression')
    def statement(self, p):
        return iteration.Repeat(p[1], p[3], p.lineno)

    @_('FOR IDENTIFIER ASSIGN expression TO expression statement_list NEXT')
    def statement(self, p):
        return iteration.For(p[1], p[3], p[5], None, p[6], p.lineno)

    @_('FOR IDENTIFIER ASSIGN expression TO expression STEP expression statement_list NEXT')
    def statement(self, p):
        return iteration.For(p[1], p[3], p[5], p[7], p[8], p.lineno)

    @_('RETURN expression')
    def statement(self, p):
        return function.Return(p[1], p.lineno)

    @_('"?" IDENTIFIER')
    def statement(self, p):
        #print(f"Got query for {p[1]}")
        return misc.QueryCommand(p[1], p.lineno)

    # Definitions for statements end here -------------------------------------------------

    # The operation is between a literal and another expression to allow chaining operators

    @_('"(" expression ")"')
    def expression(self, p):
        return p[1]
 
    @_('expresssion_operation')
    def expression(self, p):
        return p[0]

    @_('IDENTIFIER "(" arg_list ")"')
    def expression(self, p):
        return function.CallFunction(p[0], p[2], p.lineno)

    @_('IDENTIFIER "(" ")"')
    def expression(self, p):
        return function.CallFunction(p[0], None, p.lineno)

    @_('expression')
    def arg_list(self, p):
        return misc.ArgList(p[0], None)

    @_('expression "," arg_list')
    def arg_list(self, p):
        p[2] += misc.ArgList(p[0], None)
        return p[2]

    @_(
       'expression "-"      expression',
       'expression "+"      expression',
       'expression "/"      expression',
       'expression "*"      expression',
       'expression EQUAL    expression',
       'expression NOTEQUAL expression',
       'expression BIGGER   expression',
       'expression SMALLER  expression',
       'expression OR       expression',
       'expression AND      expression',
       )
    def expresssion_operation(self, p):
        #print(f"def expression_operation {p[0].name}, {p[0].type}")
        return binop.BinOp(p[0], p[1], p[2], p.lineno)


    @_('literal') # This must be added to avoid infinite recursion
    def expression(self, p):
        #print(f"found a lateral {p[0]}")
        return p[0]

    @_('"-" NUMBER %prec UMINUS')
    def literal(self, p):
        return literal.Literal(int(p[1]) * -1, "NUMBER", p.lineno)

    @_('NUMBER')  # Notice how we apply a number of grammar rules to the same method
    def literal(self, p):
        #print(f"Got literal INTEGER {p[0]}")
        return literal.Literal(int(p[0]), "NUMBER", p.lineno)

    @_('NUMBER "." NUMBER')
    def literal(self, p):
        return literal.Literal(float(f"{p[0]}.{p[2]}"), "NUMBER", p.lineno)

    @_('BOOL')
    def literal(self, p):
        return literal.Literal(True if p[0] == "TRUE" else False, "BOOLEAN", p.lineno)

    @_('STRING')  # Notice how we apply a number of grammar rules to the same method
    def literal(self, p):
        return literal.Literal(str(p[0]), "STRING", p.lineno)

    @_('IDENTIFIER "[" expression "]"')
    def literal(self, p):
        #print(f"Idenifier found on line {p.lineno}")
        return identifier.ArrayIdentifier(p[0], p[2], p.lineno)

    @_('IDENTIFIER')
    def literal(self, p):
        #print(f"Idenifier found on line {p.lineno}")
        return identifier.Identifier(p[0], p.lineno)

    @_('IDENTIFIER "[" expression "]"')
    def variable(self, p):
        return identifier.ArrayIdentifier(p[0], p[2], p.lineno)

    @_('IDENTIFIER')
    def variable(self, p):
        return identifier.Identifier(p[0], p.lineno)

    bin_op = {'+':'+', '-':'-', '*':'*', '/':'/', '>':'>', '>=':'>=', '<':'<',
              '<=':'<=', '=':'==', '<>':'!=', 'AND':'and', 'OR':'or'}

    def error(self, p):
        if p:
            raise SyntaxError(f"Parser error, line {p.lineno}, unexpected token type='{p.type}' value = '{p.value}'")
        else:
            raise SyntaxError("Unexpected end of file detected while parsing program")
