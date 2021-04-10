from sly import Lexer

class PLexer(Lexer):
    
    # This is the set of tokens we are exporting to the Parser
    tokens =    {
                    IDENTIFIER, STRING, NUMBER, OR, AND, REPEAT, UNTIL,
                    IF, THEN, ELSE, ENDIF, WHILE, DO, ENDWHILE, ASSIGN, OUTPUT, INPUT,
                    DECLARE, TYPE, BOOL, BIGGER, SMALLER, EQUAL, NOTEQUAL, PROCEDURE, ENDPROCEDURE,
                    ARRAY, OF, CALL, FUNCTION, ENDFUNCTION, RETURNS, RETURN, FOR, TO, STEP, NEXT, CASE, ENDCASE,
                    OTHERWISE,
                }

    # Any literals we did not define as tokens, will be available for usage in the Parser
    literals = {'+', '-', '/', '*', '.', '!', '(', ')', ',', ':', '?', '[', ']'}

    # Any literals we want to ignore
    ignore = ' \t'

    # The definition of each token in a regex pattern - Notice that the order MATTERS!! First match will be taken
    OR       = r'OR'
    AND      = r'AND'
    ASSIGN   = r'(<-)'
    BOOL     = r'TRUE|FALSE'
    NOTEQUAL = r'<>'
    BIGGER   = r'>=|>'
    SMALLER  = r'<=|<'
    EQUAL    = r'='

    TYPE     = r'(INTEGER|REAL|CHAR|STRING|BOOLEAN|DATE)'

    # This decorator allows us to add a logic before returning the matched token.
    @_(r"(0|[1-9][0-9]*)")
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        return t

    # Notice Identifier comes after string because most words in a string would be matched with the identifier pattern
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # define keyword tokens and make them case insensitive
    keywords = ['OUTPUT', 'IF', 'THEN', 'ELSE', 'ENDIF', 'WHILE', 'DO', 'ENDWHILE',
                'REPEAT', 'UNTIL', 'INPUT', 'DECLARE', 'PROCEDURE', 'ENDPROCEDURE',
                'ARRAY', 'OF', 'CALL', 'FUNCTION', 'ENDFUNCTION', 'RETURNS',
                'RETURN', 'FOR', 'TO', 'STEP', 'NEXT', 'CASE', 'ENDCASE',
                'OTHERWISE']

    def IDENTIFIER(self, t):
        if t.value.upper() in self.keywords :
            t.type = t.value = t.value.upper()

        elif t.value.upper() in ['INTEGER', 'REAL', 'CHAR', 'STRING', 'BOOLEAN', 'DATE']:
            t.type = 'TYPE'
            t.value = t.value.upper()

        elif t.value.upper() in ['TRUE', 'FALSE']:
            t.type = 'BOOL'
            t.value = t.value.upper()

        elif t.value.upper() == 'AND':
            t.type = t.type = 'AND'

        elif t.value.upper() == 'OR':
            t.type = t.value = 'OR'

        elif t.value.upper() == 'OTHERWISE':
            t.type = t.value = 'OTHERWISE'

        return t

    @_(r'//.*')
    def ignore_comment(self, t):
        pass

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1