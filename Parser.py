import ply.yacc as yacc
from Lexer import tokens
lineno = 0
# symbol table
table = []
scopestack = [table]
# address of the allocatable memory
curr_mem = 0
# scope for memory
mem_stack = [0]
#the number given to next temporary variable
newTemp = 0
#the number given to next Label
newLabel = 0

#returns reference to the latest scope entry of the variable with identifier 'a', if exists. else returns [False,None]
def checkid(a):
  found = False

  i = len(scopestack) - 1
  j = None

  while i >= 0 :
    temptable = scopestack[i]
    for j in temptable:
      if j is None:
        continue
      if 'identifier' in j.keys() and 'arguments' not in j.keys() and j['dimension']==[] :
        if j['identifier'] == a :
          found = True         
          break
    if found :
      break
    i -= 1
        
  return [found , j]

#to see of the identifier with name a already exists
def checkid_in_scope(a):
  found = False
  j = None
  temptable = scopestack[-1]
  for j in temptable:
    if j is None:
        continue
    if 'identifier' in j.keys():
      if j['identifier'] == a :
        found = True         
        break
        
  return found

#intermediate type casting
def type_declare(var_type, val_type, value):
  flag_err = 0
  if var_type == 'int':
    if val_type == 'char':
      value = ord(value)
    else:
      value =  (int)(value)
  if var_type == 'float':
    if val_type == 'char':
      value = ord(value)
    else:
      value =  (float)(value)
  if var_type == 'char':
    if val_type == 'int':
      value = chr(value)
    elif val_type == 'float':
      flag_err = 1
      p_error("Float cann't be assigned to char type")
  return [value, flag_err]

#checks if the array access is valid
def checkarrayid(a , isLhs = False ):
  found = False
  i = len(scopestack) - 1
  j = None
  flag = 1
  global newLabel
  global newTemp
  codeblock = None

  while i >= 0 :
    temptable = scopestack[i]
    for j in temptable:
      if 'identifier' in j.keys() and 'arguments' not in j.keys() :
        if j['identifier'] == a['identifier'] and len(j['dimension'])==len(a['dimension']):
          flag = 1
          code = []
          curType = j['type']
          cumProduct = {'tempID' : newTemp + 1, 'type' : curType}
          curIndex = {'tempID' : newTemp + 2, 'type' : curType}
          resultTemp = {'tempID' : newTemp + 3, 'type' : curType}
          #T1 = 1 cum pro
          code.append({'inst_type':'ASGN' , 'src1': {'constant': 4 , 'type':'int'} , 'src2':{}, 'dest':cumProduct})
          #T3 = 0 fin
          code.append({'inst_type':'ASGN' , 'src1': {'constant': 0 , 'type':'int'} , 'src2':{}, 'dest':resultTemp})
          for k in range(len(j['dimension'])):
            if type(a['dimension'][k]) == int:
              if j['dimension'][k] <= a['dimension'][k] :
                flag = 0
                j = a['identifier'] + 'Array out of bound'
                break
              #T2 = t1 * index //cur offset
              code.append({'inst_type': 'MUL' , 'src1': cumProduct , 'src2':{'constant': a['dimension'][k] , 'type':'int'}, 'dest':curIndex})
              #T3 = t3 + t2
              code.append({'inst_type': 'ADD' , 'src1': curIndex , 'src2':resultTemp, 'dest':resultTemp})
              #T1 = t1 * dim
              code.append({'inst_type': 'MUL' , 'src1': cumProduct , 'src2':j['dimension'][k], 'dest':cumProduct})
            
            elif type(a['dimension'][k]) == dict:
              #T4 = sgt i , dim
              code.append({'inst_type': 'SGT' , 'src1': a['dimension'][k], 'src2':j['dimension'][k] , 'dest':curIndex})
              #IF0 T4 GOTO Lnext1
              #error
              #Lnext1:
              #.
              code.append({'inst_type': 'IF0' , 'src1': curIndex, 'src2': {} , 'dest':{'Label' : 'L'+str(newLabel)}})
              code.append({'inst_type': 'ERROR' , 'src1': {}, 'src2':{} , 'dest':{}})
              code.append({'inst_type': 'LABEL' , 'src1': {}, 'src2':{} , 'dest':{'Label' : 'L'+str(newLabel)}})
              newLabel = newLabel + 1
              #T2 = t1 * index //cur offset
              code.append({'inst_type': 'MUL' , 'src1': cumProduct , 'src2':{'constant': a['dimension'][k] , 'type':'int'}, 'dest':curIndex})
              #T3 = t3 + t2
              code.append({'inst_type': 'ADD' , 'src1': curIndex , 'src2':resultTemp, 'dest':resultTemp})
              #T1 = t1 * dim
              code.append({'inst_type': 'MUL' , 'src1': cumProduct , 'src2':j['dimension'][k], 'dest':cumProduct})

          if flag == 1:
            found = True
            #t0 = a [ t3 ]
            if(isLhs):
              #send the address of the array element
              code.append({'inst_type': 'ADD' , 'src1': resultTemp , 'src2':{'constant':j['start_addr'], 'type':'int'} , 'dest':{'tempID': newTemp, 'type': j['type']}})
            else:
              #send the value of the array element
              code.append({'inst_type': 'ARRAYVAL' , 'src1': a , 'src2':resultTemp, 'dest':{'tempID': newTemp, 'type': j['type']}})
            codeblock = {'Code': code, 'PassedValue': {'tempID': newTemp, 'type': j['type']}}
            #advancing into next temporary
            newTemp = newTemp + 1
          break     

    if found or flag == 0 :
      break
    i -= 1
  return [found, j, codeblock]

#checks if function with identifier 'funcid' exists
def checkfuncdef(funcid):
  deffound = False
  for i in table:
    if 'identifier' in i.keys():
      if i['identifier'] == funcid:
        deffound = True
        break
  return deffound

#checks if function call is valid
def checkfunccall(funcid, args):
  deffound = False
  argright = False
  rettype = ''

  for i in table:
    if 'identifier' in i.keys() and 'arguments' in i.keys():
      if i['identifier'] == funcid:
        deffound = True
        rettype = i['returntype']
        if len(args) != len(i['arguments']):
          break
        count = 0
        for j in i['arguments']:
          if args[count]['type'] != j['type']:
            break
          count =  count + 1
        if count == len(i['arguments']):
          argright = True
        break
  return [deffound, argright, rettype]

#type converion
def type_conversion(p,q,r):
  ty = None
  if r['type'] != q['type']:
    if r['type']=='float' or q['type']=='float':
      ty = 'float'
    elif r['type']=='int' or q['type']=='int':
      ty = 'int'
    else:
      ty = 'char'
    p = {'type':ty}
  else:
    ty = r['type']
    p = {'type':r['type']}
  val1 = None
  val2 = None
  if 'constant' in r.keys():
    if r['type'] == 'char':
      val1 = ord(r['constant'])
    else:
      val1 = r['constant']

  #henceforth even 'value' shall be 'constant'  
  if 'constant' in q.keys():
    if q['type'] == 'char':
      val2 = ord(q['constant'])
    else:
      val2 = q['constant']

  return [ty,val2,val1, p]

#type conv log
def type_conv_log(p,q,r):
  ty = 'int'
  p = {'type':'int'}
  val1 = None
  val2 = None
  if 'constant' in r.keys():
    if r['type'] == 'char':
      val1 = ord(r['constant'])
    else:
      val1 = r['constant']

  #'value' shall be 'constant'  
  if 'constant' in q.keys():
    if q['type'] == 'char':
      val2 = ord(q['constant'])
    else:
      val2 = q['constant']

  return [ty,val2,val1, p]

def p_final(p):
  'S : prgm'
  p[0] = p[1]
  for i in p[0]['Code']:
    print(i)

def p_prgm(p):
  'prgm : prgm stmt'
  p[0] = {}
  global lineno
  lineno =lineno + 1
  code = p[1]['Code']
  code += p[2]['Code']
  p[0]['Code'] = code

def p_lastprgm(p):
  'prgm : '
  p[0] = {}
  p[0]['Code'] = []

def p_stmts(p):
  'stmt : funcdef'
  p[0] = p[1]

def p_stmt_funccall(p):
  'stmt : funccall SEMICOLON'
  p[0] = p[1]

def p_stmt_declare(p):
  'stmt : declare'
  p[0] = p[1]

def p_stmt_assign(p):
  'stmt : assign'
  p[0] = p[1]

def p_stmt_ifstmt(p):
  'stmt : ifstmt'
  p[0] = p[1]

def p_stmt_whilestmt(p):
  'stmt : whilestmt'
  p[0] = p[1]

def p_stmt_printstmt(p):
  'stmt : printstmt'
  p[0] = p[1]

def p_stmt2(p):
  'stmt2 : stmt2 stmtelt'
  p[0] = {}
  global lineno
  lineno += 1
  code = p[1]['Code']
  code += p[2]['Code']
  p[0]['Code'] = code

def p_stmt2_or(p):
  'stmt2 : '
  p[0] = {}
  p[0]['Code'] = []
  
def p_stmtelt_funccall(p):
  'stmtelt : funccall SEMICOLON'
  p[0] = p[1]

def p_stmtelt_declare(p):
  'stmtelt : declare'
  p[0] = p[1]

def p_stmtelt_assign(p):
  'stmtelt : assign'
  p[0] = p[1]

def p_stmtelt_ifstmt(p):
  'stmtelt : ifstmt'
  p[0] = p[1]

def p_stmtelt_whilestmt(p):
  'stmtelt : whilestmt'
  p[0] = p[1]

def p_stmtelt_printstmt(p):
  'stmtelt : printstmt'
  p[0] = p[1]

def p_stmtelt_returnstmt(p):
  'stmtelt : returnstmt'
  p[0] = p[1]

def p_stmtelt_continuestmt(p):
  'stmtelt : continuestmt'
  p[0] = p[1]

def p_stmtelt_breakstmt(p):
  'stmtelt : breakstmt'
  p[0] = p[1]


def p_funcdef(p):
  'funcdef : FUNCTION type IDENTIFIER funcdefy LCB nulltypeargsx RCB LFB stmt2 RFB fundefexit'
  p[0] = {}
  res = checkfuncdef(p[3])
  global newTemp
  code = []
  if res == False:
    table[p[4][0]].update({'identifier': p[3], 'returntype':p[2], 'arguments':p[6]})
    code.append({'inst_type': 'LABEL' , 'src1': {}, 'src2':{} , 'dest':{'Label' : p[3]}})
    code.append({'inst_type': 'ARGS', 'src1': {}, 'src2': {}, 'dest': p[6]})
    code += p[9]['Code']
    code += p[11]['Code']
  else:
    p_error(str(p[3]) + " Function already Exist ")
    code.append({'inst_type': 'ERROR',  'src1': {}, 'src2':{} , 'dest':{}})
  p[0]['Code'] = code
  newTemp = p[4][1]
  

def p_fundefy(p):
  'funcdefy : '
  global lineno
  global newTemp
  table.append({'lineno':lineno})
  p[0] = [len(table) - 1, newTemp]
  #lineno += 1
  table.append({'lineno':lineno, 'subtable':[]})
  scopestack.append(table[-1]['subtable'])
  mem_stack.append(curr_mem)

def p_fundefexit(p):
  'fundefexit : '
  p[0] = {}
  global curr_mem
  scopestack.pop()
  curr_mem = mem_stack[-1]
  mem_stack.pop()
  p[0]['Code'] = [{'inst_type':'EOF', 'src1': {}, 'src2': {}, 'dest': {}}]
  

def p_nulltypeargsx(p):
  'nulltypeargsx : nulltypeargs'
  currenttable = scopestack[-1]
  p[0] = p[1]
  for i in p[1]:
    currenttable.append(i)

def p_nulltypeargs(p):
  'nulltypeargs : typeargs'
  p[0] = p[1]

def p_nulltypeargs_or(p):
  'nulltypeargs : '
  p[0] = []

def p_typeargs(p):
  'typeargs : typeargs typearg'
  p[0] = p[1].append(p[2])

def p_typeargs_or(p):
  'typeargs : typearg'
  p[0] = [p[1]]

def p_typearg(p):
  'typearg : type typeargval'
  global lineno
  p[2]["size"] =  p[2]["size"]*4
  p[2].update({'type': p[1], 'lineno':lineno})
  p[0] = p[2]

def p_typeargval(p):
  'typeargval : IDENTIFIER'
  p[0] = {'identifier' : p[1], 'dimension':[], 'size': 1}

# def p_typeargval_or(p):
#   'typeargval : arrayid'
#   p[0] = p[1]


def p_expr(p):
  'expr : expr OR andterm'
  global newTemp
  p[0] = {'PassedValue' : {} }
  res = type_conv_log(p[0]['PassedValue'],p[1]['PassedValue'],p[3]['PassedValue'])
  ty = res[0]
  val1 = res[1]
  val2 = res[2] 
  p[0] = {'PassedValue' : {} }
  p[0]['PassedValue'].update(res[3])
  value = None
  if val1 != None and val2 != None:
    if p[2] == '||':
      value = (int) (val1 or val2)
    #p[0]['Code']=[{'inst_type':'ASGN', 'src1':{'constant': value, 'type': ty}, 'src2':{}, 'dest':{'tempID': newTemp, 'type':ty}}]
    p[0]['PassedValue'] = {'constant': value, 'type':ty}
    p[0]['Code'] = []
    #newTemp = newTemp + 1
  else:
    p[0].update({'Code':[]})
    p[0]['Code'] = p[1]['Code'] + p[3]['Code']
    if 'tempID' not in p[1]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[1]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[1]['PassedValue']['type']}})
      p[1]['PassedValue'] = {'tempID': newTemp, 'type': p[1]['PassedValue']['type']}
      newTemp += 1
    if 'tempID' not in p[3]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[3]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[3]['PassedValue']['type']}})
      p[3]['PassedValue'] = {'tempID': newTemp, 'type': p[3]['PassedValue']['type']}
    resultTemp = min(p[1]['PassedValue']['tempID'] , p[3]['PassedValue']['tempID'] )
    resValue = {'tempID':resultTemp , 'type':res[3]['type']}
    p[0]['Code'].append({'inst_type':'OR', 'src1':p[1]['PassedValue'] , 'src2':p[3]['PassedValue'], 'dest':resValue})
    p[0]['PassedValue'].update(resValue)
    newTemp = resultTemp + 1
  

def p_expr_or(p):
  'expr : andterm'
  #print(p[1])
  #p[0] = exprfunc(p[0], p[1])
  #print(p[0])
  p[0] = p[1]  
  #newTemp = newTemp + 1

def p_andterm(p):
  'andterm : andterm AND equalterm'
  global newTemp
  p[0] = {'PassedValue' : {} }
  res = type_conv_log(p[0]['PassedValue'],p[1]['PassedValue'],p[3]['PassedValue'])
  ty = res[0]
  val1 = res[1]
  val2 = res[2] 
  p[0]['PassedValue'].update(res[3])
  value = None
  if val1 != None and val2 != None:
    if p[2] == '&&':
      value = (int) (val1 and val2)
    p[0]['PassedValue'].update({'constant':value})
    p[0]['Code'] = []
  else:
    p[0].update({'Code':[]})
    p[0]['Code'] = p[1]['Code'] + p[3]['Code']
    if 'tempID' not in p[1]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[1]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[1]['PassedValue']['type']}})
      p[1]['PassedValue'] = {'tempID': newTemp, 'type': p[1]['PassedValue']['type']}
      newTemp += 1
    if 'tempID' not in p[3]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[3]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[3]['PassedValue']['type']}})
      p[3]['PassedValue'] = {'tempID': newTemp, 'type': p[3]['PassedValue']['type']}
    resultTemp = min(p[1]['PassedValue']['tempID'] , p[3]['PassedValue']['tempID'] )
    resValue = {'tempID':resultTemp , 'type':res[3]['type']}
    p[0]['Code'].append({'inst_type':'AND', 'src1':p[1]['PassedValue'] , 'src2':p[3]['PassedValue'], 'dest':resValue})
    p[0]['PassedValue'].update(resValue)
    newTemp = resultTemp + 1




def p_andterm_or(p):
  'andterm : equalterm'
  #print(p[1])
  #p[0] = exprfunc(p[0], p[1])
  #print(p[0])
  p[0] = p[1]


def p_equaltermval(p):
  'equalterm : equalterm LOG relopterm'
  global newTemp
  p[0] = {'PassedValue' : {} }
  res = type_conv_log(p[0]['PassedValue'],p[1]['PassedValue'],p[3]['PassedValue'])
  ty = res[0]
  val1 = res[1]
  val2 = res[2] 
  p[0] = {'PassedValue' : {} }
  p[0]['PassedValue'].update(res[3])
  value = None
  if val1 != None and val2 != None:
    if p[2] == '==':
      value = (int) (val1 == val2)
    if p[2] == '!=':
      value = (int) (val1 != val2)
    p[0]['PassedValue'].update({'constant':value})
    p[0]['Code'] = []
  else:
    p[0].update({'code':[]})
    p[0]['Code'] = p[1]['Code'] + p[3]['Code']
    if 'tempID' not in p[1]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[1]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[1]['PassedValue']['type']}})
      p[1]['PassedValue'] = {'tempID': newTemp, 'type': p[1]['PassedValue']['type']}
      newTemp += 1
    if 'tempID' not in p[3]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[3]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[3]['PassedValue']['type']}})
      p[3]['PassedValue'] = {'tempID': newTemp, 'type': p[3]['PassedValue']['type']}
    resultTemp = min(p[1]['PassedValue']['tempID'] , p[3]['PassedValue']['tempID'] )
    resValue = {'tempID':resultTemp , 'type':res[3]['type']}
    temp0 = {'tempID':newTemp , 'type':res[3]['type']}
    temp1 = {'tempID':newTemp + 1 , 'type':res[3]['type']}
    
    #p[0]-> ti      p[1]-> tj       p[3]->tk
    #  ...... 
    # sgt tj tk t0
    # slt tj tk t1
    # or t0 ti ti
    # !=.... leave it as it is
    # ==..... not ti    ti

    p[0]['Code'].append({'inst_type':'SGT', 'src1':p[1]['PassedValue'] , 'src2':p[3]['PassedValue'], 'dest':temp0})
    p[0]['Code'].append({'inst_type':'SLT', 'src1':p[1]['PassedValue'] , 'src2':p[3]['PassedValue'], 'dest':temp1})
    p[0]['Code'].append({'inst_type':'OR', 'src1':temp0 , 'src2':temp1 , 'dest':resValue})

    if p[2] == '==':
      p[0]['Code'].append({'inst_type':'NOT', 'src1':resValue , 'src2':{} , 'dest':resValue})
  
    p[0]['PassedValue'].update(resValue)
    newTemp = resultTemp + 1



def p_equalterm_or2(p):
  'equalterm : relopterm'
  #print(p[1])
  #p[0] = exprfunc(p[0], p[1])
  p[0] = p[1]

def p_relopterm(p):
  'relopterm : relopterm RELOP arithterm'
  global newTemp
  p[0] = {'PassedValue' : {} }
  res = type_conv_log(p[0]['PassedValue'],p[1]['PassedValue'],p[3]['PassedValue'])
  ty = res[0]
  val1 = res[1]
  val2 = res[2]
  p[0]['PassedValue'].update(res[3])
  value = None
  if val1 != None and val2 != None:
    if ty == 'int':
      if p[2] == '<=':
        value = (int)(val1 <= val2)
      elif p[2] == '>=':
        value = (int)(val1 >= val2)
      elif p[2] == '>':
        value = (int)(val1 > val2)
      elif p[2] == '<':
       value = (int)(val1 < val2)
    p[0]['PassedValue'].update({'constant':value})
    p[0]['Code'] = []
  else:
    p[0].update({'Code':[]})
    p[0]['Code'] = p[1]['Code'] + p[3]['Code']
    if 'tempID' not in p[1]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[1]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[1]['PassedValue']['type']}})
      p[1]['PassedValue'] = {'tempID': newTemp, 'type': p[1]['PassedValue']['type']}
      newTemp += 1
    if 'tempID' not in p[3]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[3]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[3]['PassedValue']['type']}})
      p[3]['PassedValue'] = {'tempID': newTemp, 'type': p[3]['PassedValue']['type']}
    resultTemp = min(p[1]['PassedValue']['tempID'] , p[3]['PassedValue']['tempID'] )
    resValue = {'tempID':resultTemp , 'type':res[3]['type']}

    #p[0]-> ti      p[1]-> tj       p[3]->tk
    # for >=  a>=b => !(a<b)
    #   slt tj tk ti
    #   not ti    ti
    # for <=
    #   sgt tj tk ti
    #   not ti    ti
    # for >/<
    #   slt/sgt tj tk ti 
    
    if p[2] == '>=':
      p[0]['Code'].append({'inst_type':'SLT', 'src1': p[1]['PassedValue'] ,
                                              'src2': p[3]['PassedValue'] , 
                                              'dest': resValue})
      p[0]['Code'].append({'inst_type':'NOT', 'src1':resValue , 'src2':{}, 'dest':resValue})
    elif p[2] == '<=':
      p[0]['Code'].append({'inst_type':'SGT', 'src1': p[1]['PassedValue'] ,
                                              'src2': p[3]['PassedValue'] , 
                                              'dest': resValue})
      p[0]['Code'].append({'inst_type':'NOT', 'src1':resValue , 'src2':{}, 'dest':resValue})
    if p[2] == '<':
      p[0]['Code'].append({'inst_type':'SLT', 'src1': p[1]['PassedValue'] ,
                                              'src2': p[3]['PassedValue'] , 
                                              'dest': resValue})
    elif p[2] == '>':
      p[0]['Code'].append({'inst_type':'SGT', 'src1': p[1]['PassedValue'] ,
                                              'src2': p[3]['PassedValue'] , 
                                              'dest': resValue})

    p[0]['PassedValue'].update(resValue)
    newTemp = resultTemp + 1

def p_relopterm_or(p):
  'relopterm : arithterm'
  #print(p[1])
  #p[0] = exprfunc(p[0], p[1])
  p[0] = p[1]

def p_arithterm(p):
  'arithterm : arithterm ARITHOP multerm' 
  global newTemp
  p[0] = {'PassedValue' : {} }
  res = type_conversion(p[0]['PassedValue'],p[1]['PassedValue'],p[3]['PassedValue'])
  ty = res[0]
  val1 = res[1]
  val2 = res[2]
  p[0] = {'PassedValue' : {} }
  p[0]['PassedValue'].update(res[3])
    
  value = None
  if val1 != None and val2 != None:
    if ty == 'float':
      if p[2] == '+':
        value = (float)(val1 + val2)
      elif p[2] == '-':
        value = (float)(val1 - val2)
    elif ty == 'int' or ty == 'char':
      if p[2] == '+':
        value = (int)(val1 + val2)
      elif p[2] == '-':
        value = (int)(val1 - val2)
    p[0]['PassedValue'].update({'constant':value})
    p[0]['Code'] = []
  else:
    #add/sub ti , tj , ti  
    p[0].update({'Code':[]})
    p[0]['Code'] = p[1]['Code'] + p[3]['Code']
    if 'tempID' not in p[1]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[1]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[1]['PassedValue']['type']}})
      p[1]['PassedValue'] = {'tempID': newTemp, 'type': p[1]['PassedValue']['type']}
      newTemp += 1
    if 'tempID' not in p[3]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[3]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[3]['PassedValue']['type']}})
      p[3]['PassedValue'] = {'tempID': newTemp, 'type': p[3]['PassedValue']['type']}
    resultTemp = min(p[1]['PassedValue']['tempID'] , p[3]['PassedValue']['tempID'] )
    if p[2] == '+':
      p[0]['Code'].append({'inst_type':'ADD', 'src1': p[1]['PassedValue'] ,
                                              'src2': p[3]['PassedValue'] , 
                                              'dest': {'tempID':resultTemp , 'type':res[3]['type']}})
    else:
      p[0]['Code'].append({'inst_type':'SUB', 'src1': p[1]['PassedValue'] ,
                                              'src2': p[3]['PassedValue'] , 
                                              'dest': {'tempID':resultTemp , 'type':res[3]['type']}})

    p[0]['PassedValue'].update({'tempID':resultTemp, 'type':res[3]['type']})
    newTemp = resultTemp + 1

def p_arithterm_or(p):
  'arithterm : multerm'
  #print(p[1])
  #p[0] = exprfunc(p[0], p[1])
  p[0] = p[1]
  

def p_multerm(p):
  'multerm : multerm MULTOP singleterm'
  global newTemp
  #type checking and conversion
  p[0] = {'PassedValue' : {} }
  res = type_conversion(p[0]['PassedValue'],p[1]['PassedValue'],p[3]['PassedValue'])
  ty = res[0]
  val1 = res[1]
  val2 = res[2]
  p[0]['PassedValue'].update(res[3])  
    
  value = None
  if val1 != None and val2 != None:
    if ty == 'float':
      if p[2] == '*':
        value = (float)(val1*val2)
      elif p[2] == '/':
        if val2!=0:
          value = (float)(val1/val2)
        else:
          p_error("Division by Zero Error")
    elif ty == 'int' or ty == 'char':
      if p[2] == '*':
        value = (int)(val1*val2)
      elif p[2] == '/':
        if val2!=0:
          value = (int)(val1/val2)
        else:
          p_error("Division by Zero Error")
    p[0]['PassedValue'].update({'constant':value})
    p[0]['Code'] = []
  else:
    #p[1].code      -ti
    #p[3].code      -tj
    #mul ti , tj , ti  
    p[0].update({'Code':[]})
    p[0]['Code'] = p[1]['Code'] + p[3]['Code']
    if 'tempID' not in p[1]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[1]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[1]['PassedValue']['type']}})
      p[1]['PassedValue'] = {'tempID': newTemp, 'type': p[1]['PassedValue']['type']}
      newTemp += 1
    if 'tempID' not in p[3]['PassedValue'].keys():
      p[0]['Code'].append({'inst_type':'ASGN', 'src1':p[3]['PassedValue'], 'src2':{}, 'dest':{'tempID': newTemp, 'type':p[3]['PassedValue']['type']}})
      p[3]['PassedValue'] = {'tempID': newTemp, 'type': p[3]['PassedValue']['type']}
    resultTemp = min(p[1]['PassedValue']['tempID'] , p[3]['PassedValue']['tempID'] )
    if p[2] == '*':
      p[0]['Code'].append({'inst_type':'MUL', 'src1': p[1]['PassedValue'] ,
                                              'src2': p[3]['PassedValue'] , 
                                              'dest': {'tempID':resultTemp , 'type':res[3]}})
    else:
      p[0]['Code'].append({'inst_type':'DIV', 'src1': p[1]['PassedValue'] ,
                                              'src2': p[3]['PassedValue'] , 
                                              'dest': {'tempID':resultTemp , 'type':res[3]}})

    p[0]['PassedValue'].update({'tempID':resultTemp, 'type':res[3]['type']})
    newTemp = resultTemp + 1
  

def p_multerm_or(p):
  'multerm : singleterm'
  #print(p[1])
  #p[0] = exprfunc(p[0], p[1])
  p[0] = p[1]

""" def exprfunc(p, q):
  if 'constant' in q.keys():
    p = {'type':q['type'],'value':q['constant']}
  elif 'identifier' in q.keys():
    p = {'type':q['type'],'Code':''}
  else:
    p = q
  return p """
  

# do type conversions from here on and above 

def p_singleterm(p):
  'singleterm : IDENTIFIER'
  res = checkid(p[1])
  p[0] = {}
  if res[0] == True:
    p[0]['PassedValue'] = res[1]
  else:
    p[0]['PassedValue'] = None
    p_error(p[1])
  p[0]['Code'] = []
  
    

def p_singleterm_or(p):
  'singleterm : prefix INTNUM'
  if p[1] == '-':
    p[2] = p[2] * -1
  p[0] = {'PassedValue': {'constant' : p[2],'type':'int'}}
  p[0]['Code'] = []

def p_singleterm_or2(p):
  'singleterm : prefix FLOATNUM'
  if p[1] == '-':
    p[2] = p[2] * -1
  p[0] = {'PassedValue': {'constant' : p[2],'type':'float'}}
  p[0]['Code'] = []
    

def p_singleterm_or3(p):
  'singleterm : CHARACTER'
  p[0] = {'PassedValue': {'constant' : p[1],'type':'char'}}
  p[0]['Code'] = []

def p_singleterm_or4(p):
  'singleterm : LCB expr RCB'
  p[0] = p[2]

def p_singleterm_or5(p):
  'singleterm : arrayid'
  result = checkarrayid(p[1]) 
  p[0] = {}
  if result[0] == False:
    p_error(result[1])   
  else:
    p[0]= result[2]
  p[0]['Code'] = []
  

#def p_singleterm_or6(p):
#  'singleterm : funccall'
#  p[0] = p[1]

def p_prefix(p):
  'prefix : ARITHOP'
  p[0] = p[1]

def p_prefix_or(p):
  'prefix : '
  p[0] = '+'

def p_assign(p):
  'assign : lhs ASSIGN rhs SEMICOLON'
  # must do type checking and type conversion if possible
  p[0]= {'Code':[]}
  p[0]['Code'] = p[1]['Code'] + p[3]['Code']
  #STORE stores the src1 to the variable in dest or to the address in the temp in dest
  p[0]['Code'].append({'inst_type':'STORE', 'src1':p[3]['PassedValue'] , 'src2':{}, 'dest':p[1]['PassedValue']})
  #p[1].update({'valuedict' : p[3]})

def p_lhs(p):
  'lhs : IDENTIFIER'
  result = checkid(p[1]) 
  if result[0] == False:
    p[0] = {}
    p_error("identifier not found in scope")   
  else:
    p[0] = {'PassedValue':result[1], 'Code':[]}       

def p_lhs_or(p):
  'lhs : arrayid'
  result = checkarrayid(p[1] , True) 
  if result[0] == False:
    p[0] = {}
    p_error(result[1])   
  else:
    p[0] = result[2]

def p_rhs(p):
  'rhs : inputstmt'
  p[0] = p[1] # {'value' : somvalue, 'stmttype' : 'inputstmt', 'type' : sometype}

def p_rhs_or(p):
  'rhs : expr'
  p[0] = p[1]  # {'value' : somvalue, 'stmttype' : 'expr', 'type' : sometype}

def p_rhs_or2(p):
  'rhs : funccall'
  p[0] = {}
  global newTemp
  p[0]['Code'] = p[1]['Code']   # {'value' : somvalue, 'stmttype' : 'funccall', 'type' : sometype}
  p[0]['PassedValue'] = {'tempID':newTemp , 'type':p[1]['type']}
  newTemp = newTemp+1
  #print("heeeeerrrrrreeeee")

def p_inputstmt(p):
  'inputstmt : INPUT LCB type RCB'
  global newTemp
  curValue = {'tempID':newTemp , 'type':p[3]}
  p[0] = {'Code':[]}
  p[0]['Code'].append({'inst_type':'INPUT', 'src1':{} , 'src2':{}, 'dest':curValue})
  newTemp = newTemp+1
  p[0]['PassedValue'] = curValue

def p_funccall(p):
  'funccall : IDENTIFIER LCB nullargs RCB'
  p[0] = {}
  global curr_mem
  res = checkfunccall(p[1], p[3]['PassedValue'])
  if res[0] == False:
    p[0] = {}
    p_error(str(p[1]) + " is not defined")
  elif res[1] == False:
    p[0] = {}
    p_error(str(p[1])+ " does not match signature")
  else:
    p[0] = {'PassedValue':{} , 'Code':{}}
    #p[0] = {'func': p[1], 'argvalues': p[3]}
    p[0]['Code'] = p[3]['Code']
    p[0]['Code'].append({'inst_type':'FUNCALL', 'src1':curr_mem , 'src2':p[3]['PassedValue'], 'dest':p[1]})
    p[0]['PassedValue']['type'] = res[2]
    p[0]['PassedValue']['funcReturn'] = 0

def p_nullargs(p):
  'nullargs : args'
  p[0] = p[1]

def p_nullargs_or(p):
  'nullargs : '
  p[0] = [{'PassedValue':[], 'Code':[]}]

def p_args(p):
  'args : args SEPARATORS arg'
  p[0] = {}  
  p[0]['PassedValue'] = p[1]['PassedValue']+ [p[3]['PassedValue']]
  p[0]['Code']= p[1]['Code'].append(p[3]['Code'])

def p_args_or(p):
  'args : arg'
  p[0] = {}
  p[0]['PassedValue'] = [p[1]['PassedValue']]
  p[0]['Code'] = p[1]['Code']

def p_arg(p):
  'arg : IDENTIFIER'
  res = checkid(p[1])  
  if res[0] == True:
    p[0] = {'PassedValue':res[1] , 'Code':[]}
  else:
    p[0] = {}
    p_error(p[1])  


def p_arg_or(p):
  'arg : prefix INTNUM'
  if p[1] == '-':
    p[2] = -p[2]
  p[0] = {'PassedValue':{'type' : 'int', 'constant' : p[2]} , 'Code':[]}

def p_arg_or2(p):
  'arg : prefix FLOATNUM'
  if p[1] == '-':
    p[2] = -p[2]
  p[0] = {'PassedValue':{'type' : 'float', 'constant' : p[2]} , 'Code':[]} 

def p_arg_or3(p):
  'arg : CHARACTER'
  p[0] = {'PassedValue':{'type' : 'char', 'constant' : p[1]} , 'Code':[]}

def p_arg_or4(p):
  'arg : arrayid'
  res = checkarrayid(p[1])
  if res[0] == True:
    #p[1].update({'type' : res[1]['type']})
    p[0] =  res[2]
  else:
    p[0] = {}
    p_error(p[1])

def p_ifstmt(p):
  'ifstmt  : IF LCB expr RCB LFB ifbegin stmt2 RFB ifend elsepart'
  p[0] = {}
  global newLabel, newTemp
  l1 = newLabel 
  l2 = newLabel + 1
  l3 = newLabel + 2
  newLabel += 3
  code = []
  code += p[3]['Code']
  temp = {}
  if 'constant' in p[3]['PassedValue'].keys():
    code.append({'inst_type':'ASGN' , 'src1': {'constant': p[3]['PassedValue']['constant'] , 'type':p[3]['PassedValue']['type']} , 'src2':{}, 'dest':{'tempID':newTemp, 'type':p[3]['type']}})
    temp = {'tempID':newTemp, 'type':p[3]['type']}
  else:
    temp = p[3]['PassedValue']
  code.append({'inst_type': 'IF1' , 'src1': temp, 'src2': {} , 'dest':{'Label' : 'L'+str(l1)}})
  code.append({'inst_type':'GOTO','src1': {}, 'src2': {}, 'dest': {'Label' : 'L'+str(l2)}})
  code.append({'inst_type': 'LABEL' , 'src1': {}, 'src2':{} , 'dest':{'Label' : 'L'+str(l1)}})
  code += p[7]['Code']
  code.append({'inst_type':'GOTO','src1': {}, 'src2': {}, 'dest': {'Label' : 'L'+str(l3)}})
  code.append({'inst_type': 'LABEL' , 'src1': {}, 'src2':{} , 'dest':{'Label' : 'L'+str(l2)}})
  code += p[10]['Code']
  code.append({'inst_type': 'LABEL' , 'src1': {}, 'src2':{} , 'dest':{'Label' : 'L'+str(l3)}})
  p[0]['Code'] = code
  newTemp = p[6]

def p_ifbegin(p):
  'ifbegin : '
  global lineno, newTemp
  lineno += 1
  currenttable = scopestack[-1]
  currenttable.append({'lineno':lineno, 'subtable':[]})
  scopestack.append(currenttable[-1]['subtable'])
  mem_stack.append(curr_mem)
  #capturing the temp vars that in the prev scope of if
  p[0] = newTemp

def p_ifend(p):
  'ifend : '
  global curr_mem
  curr_mem = mem_stack[-1]
  mem_stack.pop()
  scopestack.pop()

def p_elsepart(p):
  'elsepart : ELSE LFB elsebegin stmt2 RFB elseend'
  p[0] = {}
  p[0]['Code'] = p[4]['Code']
  global newTemp
  newTemp = p[3]


def p_elsebegin(p):
  'elsebegin : '
  global lineno
  lineno += 1
  currenttable = scopestack[-1]
  currenttable.append({'lineno':lineno, 'subtable':[]})
  scopestack.append(currenttable[-1]['subtable'])
  mem_stack.append(curr_mem)
  #capturing the temp vars that in the prev scope of if
  p[0] = newTemp

def p_elseend(p):
  'elseend : '
  global curr_mem
  curr_mem = mem_stack[-1]
  mem_stack.pop()
  scopestack.pop()

def p_elsepart_or(p):
  'elsepart : '
  p[0] = {}
  p[0]['Code'] = []

def p_whilestmt(p):
  'whilestmt : WHILE LCB expr RCB LFB whilebegin stmt2 RFB whileend'
  p[0] = {}
  global newLabel
  l1 = newLabel
  l2 = newLabel + 1
  newLabel += 2
  code = []
  code.append({'inst_type':'GOTO','src1': {}, 'src2': {}, 'dest': {'Label' : 'L'+str(l2)}})
  code.append({'inst_type': 'LABEL' , 'src1': {}, 'src2':{} , 'dest':{'Label' : 'L'+str(l1)}})
  code += p[7]['Code']
  code.append({'inst_type': 'LABEL' , 'src1': {}, 'src2':{} , 'dest':{'Label' : 'L'+str(l2)}})
  code += p[3]['Code']
  temp = {}
  if 'constant' in p[3]['PassedValue'].keys():
    code.append({'inst_type':'ASGN' , 'src1': {'constant': p[3]['PassedValue']['constant'] , 'type':p[3]['PassedValue']['type']} , 'src2':{}, 'dest':{'tempID':newTemp, 'type':p[3]['type']}})
    temp = {'tempID':newTemp, 'type':p[3]['type']}
  else:
    temp = p[3]['PassedValue']
  code.append({'inst_type': 'IF1' , 'src1': temp, 'src2': {} , 'dest':{'Label' : 'L'+str(l1)}})
  p[0]['Code'] = code

def p_whilebegin(p):
  'whilebegin : '
  global lineno
  lineno += 1
  currenttable = scopestack[-1]
  currenttable.append({'lineno':lineno, 'subtable':[]})
  scopestack.append(currenttable[-1]['subtable'])
  mem_stack.append(curr_mem)

def p_whileend(p):
  'whileend : '
  global curr_mem
  curr_mem = mem_stack[-1]
  mem_stack.pop()
  scopestack.pop()

def p_printstmt(p):
  'printstmt : PRINT LCB printables RCB SEMICOLON'
  p[0] = p[3]

def p_printables(p):
  'printables : printables SEPARATORS printable'
  p[0] = {}
  code = p[1]['Code']
  code += p[3]['Code']
  p[0]['Code'] = code

def p_printables_or(p):
  'printables : printable'
  p[0] = p[1]

def p_printable(p):
  'printable : STRING' 
  p[0] = {}
  code = []
  code.append({'inst_type':'PRINT', 'src1': {}, 'src2': {}, 'dest': {'value': p[1], 'type': 'string'}})
  p[0]['Code'] = code

def p_printable_or(p):
  'printable :  IDENTIFIER'
  p[0] = {}
  res = checkid(p[1])
  p[0]['Code'] = []
  if res[0] == True:
    p[0]['Code'].append({'inst_type':'PRINT', 'src1': {}, 'src2': {}, 'dest': res[1]})
  else:
    p[0] = {}
    p[0]['Code'].append({'inst_type':'ERROR', 'src1': {}, 'src2': {}, 'dest': {}})
    p_error(str(p[1]) + " Not Found")

def p_printable_and(p):
  'printable : arrayid'
  p[0] = {}
  res = checkarrayid(p[1])
  if res[0] == True:
    p[0]['Code'] = res[2]['Code']
    temp = res[2]['PassedValue']
    p[0]['Code'].append({'inst_type':'PRINT', 'src1': {}, 'src2': {}, 'dest': temp})
  else:
    p[0] = {}
    p_error(p[1] + " Not Found")
    p[0]['Code'] = [{'inst_type': 'ERROR', 'src1': {}, 'src2': {}, 'dest': {}}]
  

def p_returnstmt(p):
  'returnstmt : RETURN returnelt SEMICOLON'
  p[0] = {}
  p[0]['Code'] = p[2]['Code']

def p_returnelt(p):
  'returnelt : expr'
  p[0] = {}
  code = []
  code += p[1]['Code']
  code.append({'inst_type':'RETURN', 'src1': {}, 'src2': {}, 'dest': p[1]['PassedValue']})
  p[0]['Code'] = code

def p_returnelt_or(p):
  'returnelt : '
  p[0] = {}
  p[0]['Code'] = [{'inst_type':'RETURN', 'src1': {}, 'src2': {}, 'dest': {}}]

def p_breakstmt(p):
  'breakstmt  : BREAK SEMICOLON'
  p[0] = {}
  p[0]['Code'] = [{'inst_type':'BREAK', 'src1': {}, 'src2': {}, 'dest': {}}]

def p_continuestmt(p):
  'continuestmt : CONTINUE SEMICOLON'
  p[0] = {}
  p[0]['Code'] = [{'inst_type':'CONTINUE', 'src1': {}, 'src2': {}, 'dest': {}}]

def p_declare(p):
  'declare : decbegin type vars SEMICOLON'
  p[0] = {}
  global lineno
  global curr_mem, newTemp
  currenttable = scopestack[-1]
  code = []
  for i in p[3]:
    if i == {}:
      continue
    if checkid_in_scope(i['identifier']):
      p_error("Multiple Declaration of " + i["identifier"] )
      continue
    i["type"] = p[2]
    i["lineno"] = lineno
    i["size"] =  i["size"]*4
    i["start_addr"] = curr_mem
    curr_mem += i["size"]
    act_value = None
    if 'valuedict' in i.keys():
      if 'value' in i['valuedict'].keys():
        res = type_declare(i["type"], i['valuedict']['type'], i['valuedict']['value'])
        if res[1] == 0:
          act_value =  res[0]
          i['valuedict']['value'] = res[0]
    code += i['Code']
    if 'PassedValue' in i.keys():
      del i['Code']
      code.append({'inst_type':'DECLARE', 'src1':i['PassedValue'], 'src2':{}, 'dest':i})
      del i['PassedValue']
    else:
      del i['Code']
      code.append({'inst_type':'DECLARE', 'src1':{}, 'src2':{}, 'dest':i})
    currenttable.append(i)
  p[0]['Code'] = code
  #print(currenttable)
  newTemp = p[1]

def p_decbegin(p):
  'decbegin :'
  global newTemp
  p[0] = newTemp

def p_type(p):
  '''type : FLOAT 
  | INT 
  | CHAR '''
  p[0] = p[1]

def p_vars(p):
  'vars : var SEPARATORS vars '
  p[0] = [p[1]]
  p[0] += p[3]
  

def p_lastvars(p):
  'vars : var'  
  p[0] = [p[1]]


def p_var(p):
  'var : IDENTIFIER val'
  p[0] = {}
  res = checkid_in_scope(p[1])
  idDic = {}
  if res == False:
    p[0] = {'identifier':p[1], 'dimension':[], 'size':1}
  else:
    p[0] = {}
    p_error("Multiple Declaration of " + p[1])
  code = []
  if p[2] != {}:
    #print("hiiiiiiiiiiiiii")
    #print(p[2])
    code += p[2]['Code']
    p[0]['PassedValue'] = p[2]['PassedValue']
  p[0]['Code'] = code 
  

def p_vararray(p):
  'var : arrayvar'
  p[0] = p[1]
  p[0].update({'Code': []})

def p_arrayid_var(p):
  'arrayvar : arrayvar LSB INTNUM RSB'
  p[0] = p[1]
  p[0]['dimension'].append(p[3])
  p[0]['size'] = p[0]['size']*p[3] 

def p_arrayidlast_var(p):
  'arrayvar : IDENTIFIER LSB INTNUM RSB'
  res = checkid_in_scope(p[1])
  if res == False:
    p[0] = {'identifier':p[1] , 'dimension':[p[3]] , 'size':p[3]}
  else:
    p[0] = {}
    p_error("Multiple Declaration of "+ p[1])

def p_arrayid(p):
  'arrayid : arrayid1'
  res = checkarrayid(p[1])
  if res[0]:
    p[0] = p[1]
  else:
    p[0] = {}
    p_error(res[1])

def p_arrayid1(p):
  'arrayid1 : arrayid1 LSB index RSB'
  p[0]['dimension'].append(p[3])

def p_arrayidlast(p):
  'arrayid1 : IDENTIFIER LSB index RSB'
  p[0] = {'identifier':p[1] , 'dimension' : [p[3]]}

def p_index(p):
  'index : INTNUM'
  p[0] = p[1]

def p_index1(p):
  'index : IDENTIFIER'  
  res = checkid(p[1])
  if res[0] == True and res[1]['type'] == 'int':
    p[0] = res[1]
  else:
    p[0] = {}
    p_error("invalid array index "+ p[1])
  
def p_val(p):
  'val : ASSIGN expr'
  p[0] = p[2]  # {'value' : somvalue, 'stmttype' : 'expr', 'type' : sometype}

def p_val_or(p):
  'val : ASSIGN inputstmt'
  p[0] = p[2]  # {'value' : somvalue, 'stmttype' : 'inputstmt'}

def p_val_or2(p):
  'val : ASSIGN funccall'
  p[0] = p[2]  # {'value' : somvalue, 'stmttype' : 'funccall'}

def p_emptyval(p):
  'val : '
  p[0] = {}

def p_error(p):
  global lineno
  print(p)
  if type(p) == str:
    print(str(lineno)+ " : " + p)
  else:
    # p.value, p.type, p.lineno, p.lexpos
    print(str(lineno)+ " : Unexpected token " + str(p.value))

parser = yacc.yacc()
# data = '''
#   int sai;
#   int swe, sru;
# '''

'''s =
  int i, j = 0;
  while(i<2)
  {
    j = j+1;
    i = i+1;
    print(i,j);
  }
'''

''' 
// Sample Program of selection sort
int n, arr[10];
int i =0;
n =  input(int);
while(i<n)
{
	arr[i] = input(int);
	i=i+1;
}
int j=0,k=0;

// sorting the array

while(j<n)
{
	k = j+ 1;
	while(k<n)
	{
if(arr[j]<arr[k])
		{
			int temp = arr[j];
			arr[j] = arr[k];
			arr[k] = temp;
		}
		
k= k+1;
	}
	j = j+1;
}
// printing the array

i = 0;
while(i<n)
{
	print("Array values", i , " ",arr[i], "\n");
	i=i+1;
}

'''

s = ''' function int fibo(int n) {
	int first = 0, second = 1;
	int i = 0;
	while(i < n) {
		int third = first + second;
		print("\n", third);
		first = second;
		second = third;
	}
	return second;
}

int n = input(int);
int ans = fibo(n);
print(n, "th fibonacci:", ans);
float f = input(float);
//float result = 0;
if(f < 0 ) {
	float result = 2 * (f <= -1 && f >= -3);
	if(result == 2) {
		print("\nYay!");
	}
}
else {
	float result = -2 * (f || 1);
	if(result == -2) {
		print("\nHurray");
	}
}

'''
result = parser.parse(s)
#print(result)
for i in table:
  print(i)



#thisplace
#code.append({'inst_type':, 'src1': , 'src2':, 'dest':})