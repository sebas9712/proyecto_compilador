import ply.lex
import ply.yacc


############### LEXER ###############

# Reserved words
reserved = {
    'program': 'PROGRAMA',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'then': 'THEN',
  	'while':'WHILE',
  	'do':'DO',
  	'for':'FOR',
  	'void': 'VOID',
  	'module':'MODULE',
	'return':'RETURN',
  	'write':'WRITE',
  	'read':'READ'
}
# Token List
tokens = [
    'ID',
    'COMMENT',
    'SEMICOLON',
    'LBRACKET',
    'RBRACKET',
    'EQUAL',
    'DBEQUALS',
    'NOTEQUAL',
    'GREATERT',
    'LESST',
    'AND',
    'OR',
    'LPAREN',
    'RPAREN',
    'DOT',
    'COMA',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'CTESTRING',
    'CTEINT',
    'CTEF',
] + list(reserved.values())

t_SEMICOLON = r';'
t_LBRACKET = r'{'
t_RBRACKET = r'}'
t_EQUAL = r'='
t_DBEQUALS = r'=='
t_NOTEQUAL = r'\!=' #revisar Regex
t_GREATERT = r'>'
t_LESST = r'<'
t_AND = r'&' #Revisar Regex
t_OR = r'\|' #Revisar Regex
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DOT = r'\.'
t_COMA = r'\,'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_CTESTRING = r'".*"'
t_CTEINT = r'[1-9][0-9]*'
t_CTEF = r'[1-9][0-9]*\.[0-9]'

# Ignorar tabuladores y espacios
t_ignore = ' \t'


#Revisar si el id es una plabra reservada
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

#Revisar comentarios
def t_comment(t):
    r'\%%.*'
    pass
#Coneo de lineas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
#Manejo de errores lexicos
def t_error(t):
    print("Lexical error ' {0} ' found in line ' {1} ' ".format(t.value[0], t.lineno))
    t.lexer.skip(1)

############### PARSER ###############

#Cubo semantico



# Productions
start = 'PROGRAMA'


def p_empty(p):
    'empty :'
    pass


def p_PROGRAMA(p):
    'PROGRAMA : PROGRAM ID SEMICOLON PROGRAMA_AUX BLOQUE'
    pass


def p_PROGRAMA_AUX(p):
    '''PROGRAMA_AUX : VARS
    | empty'''
    pass


def p_VARS(p):
    'VARS : VAR VARS_AUX COLON TIPO SEMICOLON VARS_AUX2'
    pass


def p_VARS_AUX(p):
    '''VARS_AUX : ID COMA VARS_AUX
    | ID'''
    pass


def p_VARS_AUX2(p):
    '''VARS_AUX2 : VARS_AUX COLON TIPO SEMICOLON VARS_AUX2
    | empty'''
    pass


def p_TIPO(p):
    '''TIPO : INT
    | FLOAT'''
    pass


def p_BLOQUE(p):
    'BLOQUE : LBRACKET ESTATUTO_AUX RBRACKET'
    pass


def p_ESTATUTO_AUX(p):
    '''ESTATUTO_AUX : ESTATUTO ESTATUTO_AUX
    | empty'''
    pass


def p_ESTATUTO(p):
    '''ESTATUTO : ASIGNACION
    | CONDICION
    | ESCRITURA'''
    pass


def p_ASIGNACION(p):
    'ASIGNACION : ID EQUAL EXPRESION COLON'
    pass


def p_EXPRESION(p):
    'EXPRESION : EXP EXPRESION_AUX'
    pass


def p_EXPRESION_AUX(p):
    '''EXPRESION_AUX : GREATERT EXP
    | LESST EXP
    | DIFF EXPRESION
    | empty'''
    pass


def p_CONDICION(p):
    'CONDICION : IF LPAREN EXPRESION RPAREN BLOQUE CONDICION_AUX COLON'
    pass


def p_CONDICION_AUX(p):
    '''CONDICION_AUX : ELSE BLOQUE
    | empty'''
    pass


def p_ESCRITURA(p):
    'ESCRITURA : PRINT LPAREN ESCRITURA_AUX RPAREN SEMICOLON'
    pass


def p_ESCRITURA_AUX(p):
    '''ESCRITURA_AUX : EXPRESION ESCRITURA_AUX2
    | CTESTRING ESCRITURA_AUX2'''
    pass


def p_ESCRITURA_AUX2(p):
    '''ESCRITURA_AUX2 : DOT ESCRITURA_AUX
    | empty'''
    pass


def p_EXP(p):
    'EXP : TERMINO EXP_AUX'
    pass


def p_EXP_AUX(p):
    '''EXP_AUX : PLUS EXP
    | MINUS EXP
    | empty'''
    pass


def p_TERMINO(p):
    'TERMINO : FACTOR TERMINO_AUX'
    pass


def p_TERMINO_AUX(p):
    '''TERMINO_AUX : MULTIPLY TERMINO
    | DIVIDE TERMINO
    | empty'''
    pass


def p_FACTOR(p):
    '''FACTOR : LPAREN EXPRESION RPAREN
    | FACTOR_AUX'''
    pass


def p_FACTOR_AUX(p):
    '''FACTOR_AUX : PLUS VARCTE
    | MINUS VARCTE
    | VARCTE'''
    pass


def p_VARCTE(p):
    '''VARCTE : ID
    | CTEINT
    | CTEF'''
    pass


# Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Error handling rule for parser


def p_error(p):
    print("Done")
    if not p:
        print("End of File!")
        return

    while True:
        tok = parser.token()
        if not tok or tok.type == 'closebrac':
            break
    parser.restart()


# Build Lexer
lexer = ply.lex.lex()

# Build the parser
parser = ply.yacc.yacc()

# Test it out
aux = int(input("1.Programa que cumple\n2.Programa que no cumple\n3.Documento\n"))

data = ""

if(aux == 1):
    data = '''program Example;
var aux1: float; aux2: int;
{
}'''

elif(aux == 2):
    data = '''programa ~No Cumple~'''

elif(aux == 3):
    f = open("example.duck", "r")
    if f.mode == 'r':
        data = f.read()
    else:
        print("Error: input File not found or redable")


# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

result = parser.parse(data)
print(result)