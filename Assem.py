from Parser import *
import json
import sys 
#f0 for input, f0 is zero reegister, f0 is for return
#f12 is for syscall
num_int_reg = 17
# s7 for 1
# $zero is 0
num_float_reg = 27
# f31 is for our convenient use
# f29 is 1
# f30 is 0
reg_to_var = {}
freg_to_var = {}
var_to_reg = {}
var_to_freg = {}
# var can be identifier as well as temp variable
# t0 -t9, s0-s7
#register map to qtspim registers
int_reg = {}
float_reg = {}
for i in range(num_int_reg):
    if i in range(0,10):
        int_reg[i] = "$t" + str(i)
    if i in range(10, num_int_reg):
        int_reg[i] = "$s" + str(i-10)

for i in range(11):
    #f0 and f12 are reserved
    float_reg[i] = "$f" + str(i+1)
for i in range(11, num_float_reg):
    float_reg[i] = "$f" + str(i+2)


labelnum = 0
stringnum = 0
theStrings = ['.data']
theInstrs = []          #store each instruction here!

#running the parser here!


fileName = sys.argv[1]
with open(fileName , 'r') as f:
    s = f.read()
result = parser.parse(s)
#print(result)
reverseTraverse()
blockHeader = labelTable()
basicblock_gen()
codeStatus.reverse()


def first_initialise():
    global reg_to_var, freg_to_var, var_to_reg, var_to_freg
    for i in range(0, num_int_reg):
        reg_to_var[i] = {}
    for i in range(0, num_float_reg):
        freg_to_var[i] = {}

def initialise():
    global reg_to_var, freg_to_var, var_to_reg, var_to_freg
    for i in range(0, num_int_reg):
        if 'tempID' not in reg_to_var[i].keys() and reg_to_var[i]!={}:
            tempstr = json.dumps(sorted(reg_to_var[i].items()))
            reg_to_var[i] = {}
            del var_to_reg[tempstr]
    for i in range(0, num_float_reg):
        if 'tempID' not in freg_to_var[i].keys() and freg_to_var[i]!={}:
            tempstr = json.dumps(sorted(freg_to_var[i].items()))
            freg_to_var[i] = {}
            del var_to_freg[tempstr]

def get_reg(isInt):
    treg_to_var = {} 
    tvar_to_reg = {}
    tnum = 0
    shudSpill = False
    if isInt:
        treg_to_var = reg_to_var
        tvar_to_reg = var_to_reg
        tnum = num_int_reg
    else:
        treg_to_var = freg_to_var
        tvar_to_reg = var_to_freg
        tnum = num_float_reg
    for i in range(0, tnum):
        if treg_to_var[i] == {}:
            return [i, shudSpill]
            
    for i in range(0, tnum):
        var = treg_to_var[i]
        tempstr = json.dumps(sorted(var.items()))
        if tvar_to_reg[tempstr]['isTemp'] and tvar_to_reg[tempstr]['status']['NextUse'] == -1:
            return [i, shudSpill]

    for i in range(0, tnum):
        var = treg_to_var[i]
        tempstr = json.dumps(sorted(var.items()))
        if (not tvar_to_reg[tempstr]['isTemp']) and tvar_to_reg[tempstr]['status']['Status'] == 'NL':
            return [i, shudSpill]
    maxNextUse = 0
    index = 0
    for i in range(0, tnum):
        var = treg_to_var[i]
        tempstr = json.dumps(sorted(var.items()))
        if (not tvar_to_reg[tempstr]['isTemp']) and tvar_to_reg[tempstr]['status']['NextUse'] >= maxNextUse:
            maxNextUse = tvar_to_reg[tempstr]['status']['NextUse']
            index = i
    shudSpill = True
    return [index, shudSpill]
    
def spill(reg): # JUST store stmt from reg to corresponding if it is NOT temp var
    treg_to_var = {}
    treg = {}
    inst = ""
    if reg[1] == 'int':
        treg_to_var = reg_to_var
        treg = int_reg
        inst = 'sw '
    else:
        treg_to_var = freg_to_var
        treg = float_reg
        inst = 's.s '
    if 'tempID' not in treg_to_var[reg[0]].keys():
        if 'inside' in treg_to_var[reg[0]].keys():
            theInstrs.append(inst + treg[reg[0]]+ ", "+str(treg_to_var[reg[0]]['start_addr'])+"($k1)")
        else:
            theInstrs.append(inst + treg[reg[0]]+ ", "+str(treg_to_var[reg[0]]['start_addr'])+"($k0)")



def getassem(code, src1, src2, dest): # give assembly code 
    global labelnum
    global stringnum
    global theStrings
    if code['inst_type'] == 'NOT':
        if src1[1] == 'int':
            theInstrs.append("sub "+ int_reg[dest[0]] + ", $s7 , " + int_reg[src1[0]])
        elif src1[1] == 'float':
            theInstrs.append("sub.s  "+ float_reg[dest[0]] + ", $f29 , " + float_reg[src1[0]])

    elif code['inst_type'] == 'SUB':
        if src1[1] == 'int':
            theInstrs.append("sub "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src1[1] == 'float':
            theInstrs.append("sub.s  "+ float_reg[dest[0]] + ", " + float_reg[src1[0]] + " , " + float_reg[src2[0]])
    elif code['inst_type'] == 'DIV':
        if src1[1] == 'int':
            theInstrs.append("div "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src1[1] == 'float':
            theInstrs.append("div.s  "+ float_reg[dest[0]] + ", " + float_reg[src1[0]] + " , " + float_reg[src2[0]])

    elif code['inst_type'] == 'STORE':
        if 'tempID' in code['dest'].keys():
            if 'inside' in code['dest']['array'].keys():
                theInstrs.append("add "+ int_reg[dest[0]] + ", $k1 , " + int_reg[dest[0]])   
            else:
                theInstrs.append("add "+ int_reg[dest[0]] + ", $k0 , " + int_reg[dest[0]])
            if 'funcReturn' in code['src1']:
                if code['src1']['type'] == 'int':
                    theInstrs.append("sw $v0, 0(" + int_reg[dest[0]] + ")")
                elif code['src1']['type'] == 'float':
                    theInstrs.append("s.s $f0, 0(" + int_reg[dest[0]] + ")")
            else:
                if src1[1] == 'int':
                    theInstrs.append("sw " + int_reg[src1[0]]+ ", 0(" + int_reg[dest[0]] + ")")
                elif src1[1] == 'float':
                    theInstrs.append("s.s " + float_reg[src1[0]]+ ", 0(" + int_reg[dest[0]] + ")")

        elif 'identifier' in code['dest'].keys():
            if 'funcReturn' in code['src1']:
                if code['src1']['type'] == 'int':
                    theInstrs.append("move " + int_reg[dest[0]] + ", $v0")
                elif code['src1']['type'] == 'float':
                    theInstrs.append("mov.s "+  float_reg[dest[0]]+ ", $f0")
            elif 'constant' not in code['src1'].keys():
                if src1[1] == 'int':
                    theInstrs.append("move " + int_reg[dest[0]] + ", "  + int_reg[src1[0]])
                elif src1[1] == 'float':
                    theInstrs.append("mov.s " + float_reg[dest[0]]+ ", " + float_reg[src1[0]])
            else:
                if dest[1] == 'int':
                    theInstrs.append("li " + int_reg[dest[0]] + ", "  + str(code['src1']['constant']) )
                elif dest[1] == 'float':
                    theInstrs.append("li.s " + float_reg[dest[0]]+ ", " + str(float(code['src1']['constant'])) )


    elif code['inst_type'] == 'INPUT':
        if dest[1] == 'int':
            theInstrs.append("li $v0, 5")
            theInstrs.append("syscall")
            theInstrs.append('move '+ int_reg[dest[0]]+", $v0")
        if dest[1] == 'float':
            theInstrs.append("li $v0, 6")
            theInstrs.append("syscall")
            theInstrs.append('mov.s '+ float_reg[dest[0]]+", $f0")

    elif code['inst_type'] == "SLT":
        if src1[1] == 'int':
            theInstrs.append("slt "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src1[1] == 'float':
            theInstrs.append("c.lt.s " + float_reg[src1[0]]+", "+float_reg[src2[0]])
            theInstrs.append("bc1t _x"+ str(labelnum))            
            theInstrs.append("li " + int_reg[dest[0]] + ", 0")
            theInstrs.append("j _x" + str(labelnum+1))
            theInstrs.append("_x"+str(labelnum)+":")
            theInstrs.append("li " + int_reg[dest[0]] + ", 1")
            theInstrs.append("_x"+str(labelnum+1)+":")
            labelnum +=2

    elif code['inst_type'] == "SGT":
        if src1[1] == 'int':
            theInstrs.append("sgt "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src1[1] == 'float':
            theInstrs.append("c.le.s " + float_reg[src1[0]]+", "+float_reg[src2[0]])
            theInstrs.append("bc1f _x"+ str(labelnum))
            theInstrs.append("li " + int_reg[dest[0]] + ", 0")
            theInstrs.append("j _x" + str(labelnum+1))
            theInstrs.append("_x"+str(labelnum)+":")
            theInstrs.append("li " + int_reg[dest[0]] + ", 1")
            theInstrs.append("_x"+str(labelnum+1)+":")
            labelnum +=2
    elif code['inst_type'] == "FUNCALL":
        theInstrs.append("jal "+ code['dest']['Label'])

    elif code['inst_type'] == "GOTO":
        theInstrs.append("j "+ code['dest']['Label'])

    elif code['inst_type'] == "OR":
        if src1[1] == 'int':
            theInstrs.append("or "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src1[1] == 'float':
            theInstrs.append("li " + int_reg[dest[0]] + ", 0")
            theInstrs.append("c.eq.s " + float_reg[src1[0]]+", $f30")
            theInstrs.append("bc1f _x"+ str(labelnum))
            theInstrs.append("c.eq.s " + float_reg[src2[0]]+", $f30")
            theInstrs.append("bc1f _x"+ str(labelnum))
            theInstrs.append("j _x" + str(labelnum+1))
            theInstrs.append("_x"+str(labelnum)+":")
            theInstrs.append("li " + int_reg[dest[0]] + ", 1")
            theInstrs.append("_x"+str(labelnum+1)+":")
            labelnum+=2

    elif code['inst_type'] == "AND":
        if src1[1] == 'int':
            theInstrs.append("and "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src1[1] == 'float':
            theInstrs.append("li " + int_reg[dest[0]] + ", 1")
            theInstrs.append("c.eq.s " + float_reg[src1[0]]+", $f30")
            theInstrs.append("bc1t _x"+ str(labelnum))
            theInstrs.append("c.eq.s " + float_reg[src2[0]]+", $f30")
            theInstrs.append("bc1t _x"+ str(labelnum))
            theInstrs.append("j _x" + str(labelnum+1))
            theInstrs.append("_x"+str(labelnum)+":")
            theInstrs.append("li " + int_reg[dest[0]] + ", 0")
            theInstrs.append("_x"+str(labelnum+1)+":")
            labelnum+=2

    elif code['inst_type'] == "RETURN":
        if code['src1'] == {}:
            theInstrs.append('move $v0, $zero')
            theInstrs.append('li.s $f0, 0.0')
        elif 'constant' in code['src1'].keys():
            if code['src1']['type'] == 'int':
                theInstrs.append('li $v0, ' + str(code['src1']['constant']))
            elif code['src1']['type'] == 'float':
                theInstrs.append('li.s $f0, ' + str(code['src1']['constant'])) 
        elif src1[1] == 'int':
            theInstrs.append('move $v0, ' + int_reg[src1[0]])
        elif src1[1] == 'float':
            theInstrs.append('mov.s $f0, ' + float_reg[src1[0]])            
        theInstrs.append('jr $ra')

    elif code['inst_type'] == "BREAK":
        theInstrs.append("j "+ code['dest']['Label'])

    elif code['inst_type'] == "CONTINUE":
        theInstrs.append("j "+ code['dest']['Label'])

    elif code['inst_type'] == "PRINT":
        if 'value' in code['src1'].keys():
            temp = "_str" + str(stringnum) + ": .asciiz \"" + code['src1']['value'] + " \""
            theStrings.append(temp)
            theInstrs.append("li $v0, 4")
            theInstrs.append("la $a0, _str" + str(stringnum))
            theInstrs.append("syscall")
            stringnum += 1
        elif src1[1] == 'int':
            theInstrs.append("li $v0, 1")
            theInstrs.append("move $a0, " + int_reg[src1[0]])
            theInstrs.append("syscall")
        elif src1[1] == 'float':
            theInstrs.append("li $v0, 2")
            theInstrs.append("mov.s $f12, " + float_reg[src1[0]])
            theInstrs.append("syscall")
    
    elif code['inst_type'] in ["ASGN", 'DECLARE']:
        if 'constant' in code['src1'].keys():
            if dest[1] == 'int':
                theInstrs.append("li " + int_reg[dest[0]] +  ", " + str(code['src1']['constant']))
            elif dest[1] == 'float':
                theInstrs.append("li.s " + float_reg[dest[0]] +  ", " + str(float(code['src1']['constant'])))
        elif code['src1'] != {} and src1 != []:
            if dest[1] == 'int':
                theInstrs.append("move " + int_reg[dest[0]] +  ", " + int_reg[src1[0]] )
            elif dest[1] == 'float':
                theInstrs.append("mov.s " + float_reg[dest[0]] +  ", " +  float_reg[src1[0]])
    
    elif code['inst_type'] == 'ADD':
        if dest[1] == 'int':
            theInstrs.append("add "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif dest[1] == 'float':
            theInstrs.append("add.s  "+ float_reg[dest[0]] + ", " + float_reg[src1[0]] + " , " + float_reg[src2[0]])
    
    elif code['inst_type'] == 'MUL':
        if dest[1] == 'int':
            theInstrs.append("mul "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif dest[1] == 'float':
            theInstrs.append("mul.s  "+ float_reg[dest[0]] + ", " + float_reg[src1[0]] + " , " + float_reg[src2[0]])

    elif code['inst_type'] == 'IF0':
        if src1[1] == 'int':
            theInstrs.append('beqz ' + int_reg[src1[0]] + ', ' + code['dest']['Label'])
        else:
            theInstrs.append('c.eq.s ' + float_reg[src1[0]] + ', $f30')
            theInstrs.append('bc1t ' + code['dest']['Label'])

    elif code['inst_type'] == 'IF1':
        if src1[1] == 'int':
            theInstrs.append('beq ' + int_reg[src1[0]] + ', $s7, ' + code['dest']['Label'])
        else:
            theInstrs.append('c.eq.s ' + float_reg[src1[0]] + ', $f31')
            theInstrs.append('bc1t ' + code['dest']['Label'])

    elif code['inst_type'] == 'LABEL':
        if code['dest']['Label'] == 'main':
            theInstrs.append('main:')
            theInstrs.append('la $k0, _dataStart')
            theInstrs.append('li $s7, 1')
            theInstrs.append('li.s $f29, 1.0')
            theInstrs.append('li.s $f30, 0.0')
        else:
            theInstrs.append(code['dest']['Label'] + ':')

    elif code['inst_type'] == 'ARRAYVAL':
        if 'inside' in code['src1'].keys():
            theInstrs.append("addi  $a3, $k1 , " + str(code['src1']['start_addr']))
        else:
            theInstrs.append("addi  $a3, $k0 , " + str(code['src1']['start_addr']))
        theInstrs.append('add  $a3, $a3 , ' + int_reg[src2[0]])
        if dest[1] == 'int':
            theInstrs.append('lw ' + int_reg[dest[0]] + ', 0($a3)')
        else:
            theInstrs.append("l.s " + float_reg[dest[0]]+ ", 0($a3)")

    elif code['inst_type'] == 'EOF':
        theInstrs.append('jr $ra')

     
# sw r2, 0()
# lw r1, 0(t1) 

# Convert Integer to Float
# mtc1 IntReg, FRsrc
# cvt.s.w FRdest, FRsrc	
# Convert Float to Integer
# cvt.w.s FRdest, FRsrc
# mfc1 IntReg, FRdest    -- YES ALWAYS INT FIRST

def convert(toreg, fromreg): # convert stmt from one type to another
    if toreg[1] == 'int':
        theInstrs.append('cvt.w.s $f31, ' + float_reg[fromreg[0]])
        theInstrs.append('mfc1 ' + int_reg[toreg[0]] + ' , $f31')
    else:
        theInstrs.append('mtc1 ' + int_reg[fromreg[0]] + ' , $f31')
        theInstrs.append('cvt.s.w ' + float_reg[toreg[0]] + ' , $f31')



def load(reg, var): # just load stmt from addr of var accoridng to type of reg
    if 'identifier' in var.keys():
        if reg[1] == 'int':
            if 'inside' in var.keys():
                theInstrs.append("lw " + int_reg[reg[0]]+ ", "+ str(var['start_addr']) +"($k1)")
            else:
                theInstrs.append("lw " + int_reg[reg[0]]+ ", "+ str(var['start_addr']) +"($k0)")
        else:
            if 'inside' in var.keys():
                theInstrs.append("l.s " + float_reg[reg[0]]+ ", "+ str(var['start_addr']) +"($k1)")
            else:
                theInstrs.append("l.s " + float_reg[reg[0]]+ ", "+ str(var['start_addr']) +"($k0)")
                    
    

def store_args(code): # initialize a0, a1 and store args in just before funcall, currmem is in src1 of code

    theInstrs.append('li $k1, ' + str(code['src1']))
    theInstrs.append('add $k1, $k1, $k0')
    theInstrs.append('move $a3, $k1')
    theInstrs.append('li $a1, ' + str(len(code['src2'])))
    for arg in code['src2']:
        if 'constant' in arg.keys():
            if arg['type'] == 'int':
                theInstrs.append('li $a2, ' + str(arg['constant']))
                theInstrs.append('sw $a2, 0($a3)')
            else:
                theInstrs.append('li.s $f31, ' + str(float(arg['constant'])))
                theInstrs.append('s.s $f31, 0($a3)')
        elif 'tempID' in arg.keys():
            keystr = json.dumps(sorted(arg.items()))
            if arg['type'] == 'int':
                reg = var_to_reg[keystr]
                theInstrs.append('sw ' + int_reg[reg['reg']]+ ', 0($a3)')
            else:
                reg = var_to_freg[keystr]
                theInstrs.append('s.s ' + float_reg[reg['reg']]+ ', 0($a3)')
        else: # identifier
            keystr = json.dumps(sorted(arg.items()))
            if arg['type'] == 'int':
                if keystr not in var_to_reg.keys():
                    theInstrs.append("addi  $a2, $k0, " + str(arg['start_addr']))
                    theInstrs.append('lw $a2, 0($a2)')
                    theInstrs.append('sw $a2, 0($a3)')
                else:
                    reg = var_to_reg[keystr]
                    theInstrs.append('sw ' + int_reg[reg['reg']]+ ', 0($a3)')               
            else:
                if keystr not in var_to_freg.keys():
                    theInstrs.append("addi  $a2, $k0, " + str(arg['start_addr']))
                    theInstrs.append('l.s $f31, 0($a2)')
                    theInstrs.append('s.s $f31, 0($a3)')
                else:
                    reg = var_to_freg[keystr]
                    theInstrs.append('s.s ' + float_reg[reg['reg']]+ ', 0($a3)')
        theInstrs.append('addi $a3, $a3, 4')


def load_arg(reg, count): # load from addr a0 + count*4 in funcdef
    if count == 0:
        theInstrs.append('move $a3, $k1')    
    if reg[1] == 'int':
        theInstrs.append('lw ' + int_reg[reg[0]] + ', 0($a3)')
    else:
        theInstrs.append('l.s ' + float_reg[reg[0]] + ', 0($a3)')
    theInstrs.append('addi $a3, $a3, 4')


var_modified = {} # variable modified but not stored back, so they need storing back, same structure as var_to_reg
first_initialise()

#print("basic basic")
#print(blockHeader)

for i in range(len(theCode)):
    """
    print("___________________")
    print(theCode[i])
    
    c = 0
    for i2 in var_to_reg:
        print(i2)
    print("__________________")
    for i2 in reg_to_var :
        if reg_to_var[i2]!={}:
            c += 1
            print(reg_to_var[i2])
    print("__________________")
    print(len(var_to_reg))
    print(c)
    print("******************************") """
    if codeStatus[i] == {}:
        if theCode[i]['inst_type'] in ['GOTO', 'EOF', 'BREAK', 'CONTINUE', 'LABEL']:
            for var in var_modified.keys():
                spill(var_modified[var])
            #print("hi and start of block3")
            getassem(theCode[i], -1, -1, -1)
            var_modified = {}
            initialise()
        elif theCode[i]['inst_type'] == 'FUNCALL':
            store_args(theCode[i])
            for var in var_modified.keys():
                spill(var_modified[var])
            getassem(theCode[i], -1, -1, -1)
            var_to_modified = {}
            initialise()
            #print("hi and start of block4")
        else:
            getassem(theCode[i], -1, -1, -1)
        continue
    if theCode[i]['inst_type'] in ['IF0', 'IFEQL', 'IF1']:
        for var in var_modified.keys():
            spill(var_modified[var])
    reg_src = {}
    reg_dest = []
    dest = 'dest'
    for src in ['src1', 'src2']:
        reg_src[src] = []
        if src in codeStatus[i].keys():
            if theCode[i][src]['type'] != 'float':
                tempstr = json.dumps(sorted(theCode[i][src].items()))
                entry = theCode[i][src]
                if 'array' in theCode[i][src].keys():
                    entry = theCode[i][src].copy()
                    del entry['array']
                    tempstr = json.dumps(sorted(entry.items()))
                if 'dest' in codeStatus[i] and theCode[i]['dest']['type'] == 'float':
                    result = get_reg(False)
                    if result[1]:
                        spill([result[0], 'float'])
                    if freg_to_var[result[0]] != {}:
                        keystr = json.dumps(sorted(freg_to_var[result[0]].items()))
                        if keystr in var_modified.keys():
                            del var_modified[keystr]
                        del var_to_freg[keystr]
                    var_to_freg[tempstr] = {
                        'reg': result[0],
                        'status': {'NextUse': -1, 'Status': 'NL'},
                        'isTemp': True
                    }
                    reg_src.update({src : [result[0], 'float']})
                    if tempstr in var_to_reg.keys():
                        convert(reg_src[src], [var_to_reg[tempstr]['reg'], 'int'])
                    else:
                        load(reg_src[src], theCode[i][src])
                    freg_to_var[reg_src[src][0]] = entry
                else: 
                    if tempstr in var_to_reg.keys():
                        reg_src.update({src: [var_to_reg[tempstr]['reg'], 'int']})
                        var_to_reg[tempstr].update({'status': codeStatus[i][src]})
                        var_to_reg[tempstr].update({'isTemp': 'tempID' in theCode[i][src]})
                    else:
                        result = get_reg(True)
                        if result[1]:
                            spill([result[0], 'int'])
                        if reg_to_var[result[0]] != {}:
                            keystr = json.dumps(sorted(reg_to_var[result[0]].items()))
                            if keystr in var_modified.keys():
                                del var_modified[keystr]
                            del var_to_reg[keystr]
                        var_to_reg[tempstr] = {
                            'reg': result[0],
                            'status': codeStatus[i][src],
                            'isTemp': 'tempID' in theCode[i][src]
                        }
                        reg_src.update({src: [result[0], 'int']}) 
                        reg_to_var[reg_src[src][0]] = theCode[i][src]
                        load(reg_src[src], theCode[i][src])
            else: # if src is float 
                tempstr = json.dumps(sorted(theCode[i][src].items()))
                entry = theCode[i][src]
                if 'array' in theCode[i][src].keys():
                    entry = theCode[i][src].copy()
                    del entry['array']
                    tempstr = json.dumps(sorted(entry.items()))
                if 'dest' in codeStatus[i] and theCode[i]['dest']['type'] == 'int':
                    result = get_reg(True)
                    if result[1]:
                        spill([result[0], 'int'])
                    if reg_to_var[result[0]] != {}:
                        keystr = json.dumps(sorted(reg_to_var[result[0]].items()))
                        if keystr in var_modified.keys():
                            del var_modified[keystr]
                        del var_to_reg[keystr]
                    var_to_reg[tempstr] = {
                        'reg': result[0],
                        'status': {'NextUse': -1, 'Status': 'NL'},
                        'isTemp': True
                    }
                    reg_src.update({src : [result[0], 'int']})
                    if tempstr in var_to_reg.keys():
                        convert(reg_src[src], [var_to_freg[tempstr]['reg'], 'float'])
                    else:
                        load(reg_src[src], theCode[i][src])
                    reg_to_var[reg_src[src][0]] = entry
                else: 
                    if tempstr in var_to_freg.keys():
                        reg_src.update({src: [var_to_freg[tempstr]['reg'], 'float']})  
                        var_to_freg[tempstr].update({'status': codeStatus[i][src]})
                        var_to_freg[tempstr].update({'isTemp': 'tempID' in theCode[i][src]})
                    else:
                        result = get_reg(False)
                        if result[1]:
                            spill([result[0], 'float'])
                        if freg_to_var[result[0]] != {}:
                            keystr = json.dumps(sorted(freg_to_var[result[0]].items()))
                            if keystr in var_modified.keys():
                                del var_modified[keystr]
                            del var_to_freg[keystr]
                        var_to_freg[tempstr] = {
                            'reg': result[0],
                            'status': codeStatus[i][src],
                            'isTemp': 'tempID' in theCode[i][src]
                        }
                        reg_src.update({src: [result[0], 'float']})  
                        freg_to_var[reg_src[src][0]] = entry
                        load(reg_src[src], theCode[i][src])

    isDestList = False
    if 'dest' in codeStatus[i].keys():
        if theCode[i]['inst_type']=='DECLARE' and theCode[i]['src1'] == {}:
            continue
        if type(codeStatus[i]['dest']) == dict:
            tvar_to_reg = {}
            treg_to_var = {}
            tnum = 0
            tempstr = json.dumps(sorted(theCode[i][dest].items()))
            entry = theCode[i][dest]
            if 'array' in theCode[i]['dest'].keys():
                entry = theCode[i]['dest'].copy()
                del entry['array']
                tempstr = json.dumps(sorted(entry.items()))
            if theCode[i][dest]['type'] == 'float':
                tvar_to_reg = var_to_freg
                treg_to_var = freg_to_var
                tnum = num_float_reg
            else:
                tvar_to_reg = var_to_reg
                treg_to_var = reg_to_var
                tnum = num_int_reg
            if tempstr in tvar_to_reg.keys():
                reg_dest = [tvar_to_reg[tempstr]['reg'], theCode[i][dest]['type']]
                tvar_to_reg[tempstr].update({'status': codeStatus[i][dest]})
                tvar_to_reg[tempstr].update({'isTemp': 'tempID' in theCode[i][dest]})
            else:
                result = get_reg(theCode[i][dest]['type'] == 'int')
                reg_dest = [result[0], theCode[i][dest]['type']]
                if result[1]:
                    spill(reg_dest)
                if treg_to_var[result[0]] != {}:
                    keystr = json.dumps(sorted(treg_to_var[result[0]].items()))
                    if keystr in var_modified.keys():
                        del var_modified[keystr]
                    del tvar_to_reg[keystr]
                tvar_to_reg[tempstr] = {
                    'reg': result[0],
                    'status': codeStatus[i][dest],
                    'isTemp': 'tempID' in theCode[i][dest]
                }                
                treg_to_var[reg_dest[0]] = entry
            if 'identifier' in theCode[i][dest].keys():
                var_modified[tempstr] = reg_dest
        else: # ARGS inst
            isDestList = True
            count = 0
            for arg in theCode[i]['dest']:
                tvar_to_reg = {}
                treg_to_var = {}
                tnum = 0
                tempstr = json.dumps(sorted(arg.items()))
                if arg['type'] == 'float':
                    tvar_to_reg = var_to_freg
                    treg_to_var = freg_to_var
                    tnum = num_float_reg
                else:
                    tvar_to_reg = var_to_reg
                    treg_to_var = reg_to_var
                    tnum = num_int_reg
                result = get_reg(arg['type'] == 'int')
                reg_dest = [result[0], arg['type']]
                if result[1]:
                    spill(reg_dest)
                if treg_to_var[result[0]] != {}:
                    keystr = json.dumps(sorted(treg_to_var[result[0]].items()))
                    if keystr in var_modified.keys():
                        del var_modified[keystr]
                    del tvar_to_reg[keystr]
                tvar_to_reg[tempstr] = {
                    'reg': result[0],
                    'status': codeStatus[i][dest][count],
                    'isTemp': 'tempID' in arg
                }
                 
                treg_to_var[reg_dest[0]] = arg
                load_arg(reg_dest, count)
                count += 1
    if not isDestList:
        getassem(theCode[i], reg_src['src1'], reg_src['src2'], reg_dest)

    if theCode[i]['inst_type'] in ['IF0', 'IFEQL', 'IF1', 'RETURN']:
        var_modified = {}  
        initialise()
        #print("hi and start of block1")
    elif i+1 in blockHeader:
        var_modified = {}  
        initialise()
        #print("hi and start of block")

theStrings.append('_wordAlign: .word 0')
theStrings.append('_dataStart: .space 4096')
theStrings.append('.text ' )
theStrings.append('.globl main ' )
theStrings += theInstrs
theStrings.append('jr $ra')
f = open('Result.asm' , 'w')

for line in theStrings:
    f.write(line)
    f.write('\n')

f.close()





