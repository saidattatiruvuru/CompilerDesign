%%writefile ourLexer.py 

import ply.lex as lex

reserved = {
  'if' : 'IF',
  'else' : 'ELSE',
  'input' : 'INPUT',
  'break' : 'BREAK',
  'continue' : 'CONTINUE',
  'return' : 'RETURN',
  'function' : 'FUNCTION',
  'void' : 'VOID',
  'float' : 'FLOAT',
  'int' : 'INT',
  'while' : 'WHILE',
  'print' : 'PRINT',
  'char' : 'CHAR'
}

tokens = [
  'LFB',
  'RFB',
  'COMMENTS',
  'IDENTIFIER',
  'FLOATNUM',
  'INTNUM',
  'STRING',
  'RELOP',
  'ARITHOP',
  'LCB',
  'RCB',
  'LSB',
  'RSB',
  'OR',
  'AND',
  'LOG',
  'MULTOP',
  'SEMICOLON',
  'ASSIGN',
  'NOT',
  'CHARACTER', #CHARACTER VALUE   
  'SEPARATORS'
] + list(reserved.values())

# Regular expression rules for simple tokens

#The keywords
'''
t_INPUT= r'input'
t_BREAK= r'break'
t_CONTINUE= r'continue'
t_RETURN= r'return'
t_ELSE= r'else'
t_FUNCTION= r'function'
t_IF= r'if'
t_VOID= r'void'
t_FLOAT= r'float'
t_INT= r'int'
t_WHILE= r'while'
t_PRINT= r'print'
t_CHAR = r'char'
'''

# A string containing ignored characters (spaces and tabs) and comments
def t_COMMENT(t):
    r'//[^\n]*'
    pass
t_ignore  = ' \t'

def t_IDENTIFIER(t):
  r'[a-zA_Z_]\w*'
  t.type = reserved.get(t.value,'IDENTIFIER') 
  return t
  
def t_FLOATNUM(t):
  r'\d+\.\d+'
  t.value = float(t.value)
  return t
def t_INTNUM(t):
  r'\d+'
  t.value = int(t.value)
  return t
def t_CHARACTER(t):
  r'\'(\s|\S)\''
  l = len(t.value)
  t.value = t.value[1:(l-1)]
  return t
def t_STRING(t):
  r'\"[^\"]*\"' 
  l = len(t.value)
  t.value = t.value[1:l-1]
  return t


t_LCB  = r'\('
t_RCB  = r'\)'
t_LFB = r'\{'
t_RFB = r'\}'
t_LSB = r'\['
t_RSB = r'\]'


t_SEPARATORS = r','
t_SEMICOLON=   r';'
t_MULTOP=   r'\*|/'
t_LOG=   r'!= | =='
t_AND=   r'&&'
t_OR=   r'\|\|'
t_RELOP = r'(>= |<=|<|>)'
t_ARITHOP = r'(\+|-)'
t_ASSIGN=   r'='
t_NOT=   r'!'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
function int fibo(int n) {
	int first = 0, second = 1;
	int i = 0;
  while(i < n) {
		int third = first + second;
    //print(" lfjbvkmn", third);
		first = second;
		second = third;
    int saidatta;
	}
	return second;
}
int n = input(int);
int ans = fibo(n);
//print(n, "th fibonacci:", ans);
float f = input(float);
float result = 0;
if(f < 0 ) {
	result = 2 * (f <= -1 && f >= -3);
	if(result == 2) {
		//print("Yay!");
	}
}
else {
	result = -2 * (f || 1);
	if(result == -2) {
		print("\nHurray");
	}
}
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)

