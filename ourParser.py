%%writefile ourParser.py 
import ply.yacc as yacc
from ourLexer import tokens
lineno = 0
table = []
scopestack = []

def p_prgm(p):
  'prgm : prgm stmts'

def p_lastprgm(p):
  'prgm: '

def p_stmts(p):
  'stmts : funcdef'

def p_stmts_or(p):
  'stmts : stmt'

def p_stmt2(p):
  'stmt2 : stmt2 stmtelt'

def p_stmt2_or(p):
  'stmt2 : '

def p_stmt_funccall(p):
  'stmt : funccall'

def p_stmt_declare(p):
  'stmt : declare'

def p_stmt_assign(p):
  'stmt : assign'

def p_stmt_ifstmt(p):
  'stmt : ifstmt'

def p_stmt_whilestmt(p):
  'stmt : whilestmt'

def p_stmt_printstmt(p):
  'stmt : printstmt'

def p_stmtelt_funccall(p):
  'stmtelt : funccall'

def p_stmtelt_declare(p):
  'stmtelt : declare'

def p_stmtelt_assign(p):
  'stmtelt : assign'

def p_stmtelt_ifstmt(p):
  'stmtelt : ifstmt'

def p_stmtelt_whilestmt(p):
  'stmtelt : whilestmt'

def p_stmtelt_printstmt(p):
  'stmtelt : printstmt'

def p_stmtelt_returnstmt(p):
  'stmtelt : returnstmt'

def p_stmtelt_continuestmt(p):
  'stmtelt : continuestmt'

def p_stmtelt_breakstmt(p):
  'stmtelt : breakstmt'

def p_funcdef(p):
  'funcdef : FUNCTION type IDENTIFIER LCB nulltypeargs RCB LFB stmt2 RFB'

def p_nulltypeargs(p):
  'nulltypeargs : typeargs'


def p_nulltypeargs_or(p):
  'nulltypeargs : '

def p_typeargs(p):
  'typeargs : typeargs typearg'

def p_typeargs_or(p):
  'typeargs : typearg'

def p_typearg(p):
  'typearg : type typeargval'

def p_typeargval(p):
  'typeargval : IDENTIFIER'

def p_typeargval_or(p):
  'typeargval : arrayid'

def p_expr(p):
  'expr : expr OR andterm'

def p_expr_or(p):
  'expr : andterm'

def p_andterm(p):
  'andterm : andterm AND equalterm'  

def p_andterm_or(p):
  'andterm : equalterm'

def p_equalterm(p):
  'equalterm : equalterm equaltermval'  

def p_equaltermval(p):
  'equaltermval : EQUAL relopterm'

def p_equaltermval_or(p):
  'equaltermval : NOTEQUAL relopterm'

def p_equalterm_or2(p):
  'equalterm : relopterm'

def p_relopterm(p):
  'relopterm : relopterm RELOP arithterm'  

def p_relopterm_or(p):
  'relopterm : arithterm'

def p_arithterm(p):
  'arithterm : arithterm ARITHOP multerm'  

def p_arithterm_or(p):
  'arithterm : multerm'

def p_singleterm(p):
  'singleterm : IDENTIFIER'  

def p_singleterm_or(p):
  'singleterm : prefix INTNUM'

def p_singleterm_or2(p):
  'singleterm : prefix FLOATNUM'  

def p_singleterm_or3(p):
  'singleterm : CHARACTER'

def p_singleterm_or4(p):
  'singleterm : LCB expr RCB'  

def p_singleterm_or5(p):
  'singleterm : arrayid'

def p_singleterm_or6(p):
  'singleterm : funccall'

def p_prefix(p):
  'prefix : ARITHOP'

def p_prefix_or(p):
  'prefix : '

def p_assign(p):
  'assign : lhs ASSIGN rhs SEMICOLON'

def p_lhs(p):
  'lhs : IDENTIFIER'

def p_lhs_or(p):
  'lhs : arrayid'

def p_rhs(p):
  'rhs : inputstmt'

def p_rhs_or(p):
  'rhs : expr'

def p_inputstmt(p):
  'inputstmt : INPUT LCB type RCB'

def p_funccall(p):
  'funccall : IDENTIFIER LCB nullargs RCB SEMICOLON'

def p_nullargs(p):
  'nullargs : args'

def p_nullargs_or(p):
  'nullargs : '

def p_args(p):
  'args : args SEPARATORS arg'

def p_args_or(p):
  'args : arg'

def p_arg(p):
  'arg : IDENTIFIER'  

def p_arg_or(p):
  'arg : prefix INTNUM'

def p_arg_or2(p):
  'arg : prefix FLOATNUM'  

def p_arg_or3(p):
  'arg : CHARACTER'

def p_arg_or4(p):
  'arg : arrayid'

def p_ifstmt(p):
  'ifstmt  : IF LCB expr RCB LFB stmt2 RFB elsepart'

def p_elsepart(p):
  'elsepart : ELSE LFB stmt2 RFB'

def p_elsepart_or(p):
  'elsepart : '

def p_whilestmt(p):
  'whilestmt : WHILE LCB expr RCB LFB stmt2 RFB'

def p_printstmt(p):
  'printstmt : PRINT LCB printables RCB SEMICOLON'

def p_printables(p):
  'printables : printables SEPARATORS printable'

def p_printables_or(p):
  'printables : printable'

def p_printable(p):
  'printable : STRING' 

def p_printable(p):
  'printable :  IDENTIFIER'

def p_printable(p):
  'printable : arrayid'

def p_returnstmt(p):
  'returnstmt : RETURN returnelt SEMICOLON'

def p_returnelt(p):
  'returnelt : expr'

def p_returnelt_or(p):
  'returnelt : '

def p_breakstmt(p):
  'breakstmt  : BREAK SEMICOLON'

def p_continuestmt(p):
  'continuestmt : CONTINUE SEMICOLON'

def p_declare(p):
  'declare : type vars SEMICOLON'
  currenttable = table
  for i in scopestack:
    currenttable = currenttable[i]
  for i in p[2]:
    i["type"] = p[1]
    i["lineno"] = lineno
    if p[1]=="int" or p[1]=="float":
      i["size"] =  i["size"]*4
    else:
      i["size"] =  i["size"]*1
    currenttable.append(i)

def p_type(p):
  '''type : FLOAT 
  | INT 
  | CHAR '''
  p[0] = p[1]

def p_vars(p):
  'vars : var SEPARATORS vars '
  p[0] = p[3]
  p[0].append(p[1])
  

def p_lastvars(p):
  'vars : var'  
  p[0] = [p[1]]

def p_var(p):
  'var : IDENTIFIER val'
  p[0] = {'identifier':p[1], 'size':1}

def p_vararray(p):
  'var : arrayid'
  p[0] = p[1]


def p_arrayid(p):
  'arrayid : arrayid LSB INTNUM RSB'
  p[0] = p[1]
  p[0]['dimension'].append(p[3])
  p[0]['size'] = p[0]['size']*p[3] 

def p_arrayidlast(p):
  'arrayid : IDENTIFIER LSB INTNUM RSB'
  p[0] = {'identifier':p[1] , 'dimension':[p[3]] , 'size':p[3]}

def p_val(p):
  '''val : EQUAL expression 
  | EQUAL inputstmt'''
  p[0] = p[2]

def p_emptyval(p):
  'val : '

'''
def p_expression(p):
  'expression : IDENTIFIER'
  p[0] = 10

def p_inputstmt(p):
  'inputstmt : IDENTIFIER'
  p[0] = 10
'''


def p_error(p):
  print("gone")

parser = yacc.yacc()
# data = '''
#   int sai;
#   int swe, sru;
# '''

while True:
  try:
      s = input('calc > ')
  except EOFError:
      break
  if not s: continue
  result = parser.parse(s)
  print(result)
  print(table)
