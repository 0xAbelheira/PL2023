import ply.lex as lex

states = (
    ('comment', 'exclusive'),
)


tokens = (
    'OPEN_COMMENT_MULTI_LINE',
    'CLOSE_COMMENT_MULTI_LINE',
    'COMMENT_MULTI_LINE',
    'OPEN_COMMENT_LINE',
    'CLOSE_COMMENT_LINE'
    'COMMENT_LINE',
    'FUNC',
    'FUNCNAME',
    'PROGRAM',
    'PROGRAMNAME',
    'IF',
    'WHILE',
    'FOR',
    'IN',
    'OP',
    'COMP',
    'ASSIGN',
    'TYPE',
    'COMMA',
    'SEMICOLON',
    'PAROPEN',
    'PARCLOSE',
    'BRACKETOPEN',
    'BRACKETCLOSE',
    'SBRACKETOPEN',
    'SBRACKETCLOSE',
    'RETS',
    'NUMBER',
    'VAR'
)


t_PAROPEN = r'\('
t_PARCLOSE= r'\)'
t_BRACKETOPEN = r'\{'
t_BRACKETCLOSE = r'\}'
t_SBRACKETOPEN = r'\['
t_SBRACKETCLOSE = r'\]'
t_RETS = r'\.\.'
t_ASSIGN = r'\='
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_OP = r'[\+\-\*]'
t_TYPE = r'\b(int|boolean|float|double|long|string)\b'
t_FUNCNAME = r'[a-z_]+\w*(?=\()'
t_PROGRAMNAME = r'(?<=program\ )[a-z_]+\w*'
t_VAR = r'\w+'
t_NUMBER = r'\d+'


def t_FUNC(t):
    r'\bfunction\b'
    return t


def t_PROGRAM(t):
    r'\bprogram\b'
    return t


def t_WHILE(t):
    r'\bwhile\b'
    return t


def t_IF(t):
    r'\bif\b'
    return t


def t_FOR(t):
    r'\bfor\b'
    return t


def t_IN(t):
    r'\bin\b'
    return t


def t_COMP(t):
    r'<=|>=|<|>'
    return t
    

def t_OPEN_COMMENT_MULTI_LINE(t):
    r'\/\*'
    t.lexer.begin('comment')
    return t


def t_OPEN_COMMENT_LINE(t):
    r'\/\/'
    t.lexer.begin('comment')
    return t

    
def t_comment_CLOSE_COMMENT_MULTI_LINE(t):
    r'\*\/'
    t.lexer.begin('INITIAL')
    return t


def t_comment_CLOSE_COMMENT_LINE(t):
    r'\n+'
    t.lexer.begin('INITIAL')
    return t


def t_comment_COMMENT_LINE(t):
    r'(?<=\/\/).*'
    return t


def t_comment_COMMENT_MULTI_LINE(t):
    r'(.|\n)*?(?=\*\/)'
    return t


def t_ANY_error(t):
    print(f"Invalid Character: {t.value[0]}")
    t.lexer.skip(1)


t_comment_ignore = ''
t_INITIAL_ignore = ' \t\n'


lexer = lex.lex()

data = '''
/* factorial.p
-- 2023-03-20 
-- by jcr
*/
int i;
// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}
// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}
'''

lexer.input(data)


while tok := lexer.token():
    print(tok)