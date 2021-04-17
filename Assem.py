from Parser import *
import json
#f0 for input, f0 is zero reegister, f0 is for return
#f12 is for syscall
num_int_reg = 18
num_float_reg = 30
reg_to_var = {}
freg_to_var = {}
var_to_reg = {}
var_to_freg = {}
# var can be identifier as well as temp variable
# t0 -t9, s0-s7
#register map to qtspim registers
int_reg = {}
float_reg = {}
for i in range(18):
    if i in range(0,10):
        int_reg[i] = "$t" + str(i)
    if i in range(10, num_int_reg):
        int_reg[i] = "$s" + str(i-10)

for i in range(11):
    #f0 and f12 are reserved
    float_reg[i] = "$f" + str(i+1)
for i in range(11, num_float_reg):
    float_reg[i] = "$f" + str(i+2)


def initialise():
    for i in range(0, num_int_reg):
        reg_to_var[i] = {}
    for i in range(0, num_float_reg):
        freg_to_var[i] = {}

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
    print('spill', end="  ")
    print(reg)
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
    if 'tempID' not in treg_to_var.keys():
        print("addi  $a3, $k0 , " + str(treg_to_var['start_addr']))
        print(inst + treg[reg[0]]+ ", 0($a3)")

labelnum = 0
stringnum = 0
theStrings = []
def getassem(code, src1, src2, dest): # give assembly code 
    global labelnum
    global stringnum
    global theStrings
    print('getassem')
    print(src1, end="  ")
    print(src2, end="  ")
    print(dest, end="\n======\n")
    if code['inst_type'] == 'NOT':
        if src1[1] == 'int':
            print("li "+ int_reg[dest[0]] + ", 1")
            print("sub "+ int_reg[dest[0]] + ", " + int_reg[dest[0]] + " , " + int_reg[src1[0]])
        elif src[1] == 'float':
            print("li.s "+ float_reg[dest[0]] + " ,1.0")
            print("sub.s  "+ float_reg[dest[0]] + ", " + float_reg[dest[0]] + " , " + float_reg[src1[0]])

    elif code['inst_type'] == 'SUB':
        if src1[1] == 'int':
            print("sub "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src[1] == 'float':
            print("sub.s  "+ float_reg[dest[0]] + ", " + float_reg[src1[0]] + " , " + float_reg[src2[0]])
    elif code['inst_type'] == 'DIV':
        if src1[1] == 'int':
            print("div "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src[1] == 'float':
            print("div.s  "+ float_reg[dest[0]] + ", " + float_reg[src1[0]] + " , " + float_reg[src2[0]])
    elif code['inst_type'] == 'STORE':
        if 'tempID' in code['dest'].keys():
            print("add "+ int_reg[dest[0]] + ", $k0 , " + int_reg[dest[0]])
            if src1[1] == 'int':
                print("sw " + int_reg[src1[0]]+ ", 0(" + int_reg[dest[0]] + ")")
            elif src1[1] == 'float':
                print("s.s " + float_reg[src1[0]]+ ", 0(" + int_reg[dest[0]] + ")")
        if 'identifier' in code['dest'].keys():
            if src1[1] == 'int':
                print("sw " + int_reg[src1[0]]+ ", " + int_reg[dest[0]])
            elif src1[1] == 'float':
                print("s.s " + float_reg[src1[0]]+ ", " + float_reg[dest[0]])

    elif code['inst_type'] == 'INPUT':
        if dest[1] == 'int':
            print("li $v0, 5")
            print("syscall")
            print('move '+ int_reg[dest[0]]+", $v0")
        if dest[1] == 'float':
            print("li $v0, 6")
            print("syscall")
            print('mov.s '+ float_reg[dest[0]]+", $f0")

    elif code['inst_type'] == "SLT":
        if src1[1] == 'int':
            print("slt "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src[1] == 'float':
            print("c.lt.s " + float_reg[src1[0]]+", "+float_reg[src2[0]])
            print("bc1t _x"+ str(labelnum))            
            print("li " + int_reg[dest[0]] + ", 0")
            print("j _x" + str(labelnum+1))
            print("_x"+str(labelnum)+":")
            print("li " + int_reg[dest[0]] + ", 1")
            print("_x"+str(labelnum+1)+":")
            labelnum +=2

    elif code['inst_type'] == "SGT":
        if src1[1] == 'int':
            print("sgt "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src[1] == 'float':
            print("c.le.s " + float_reg[src1[0]]+", "+float_reg[src2[0]])
            print("bc1f _x"+ str(labelnum))
            print("li " + int_reg[dest[0]] + ", 0")
            print("j _x" + str(labelnum+1))
            print("_x"+str(labelnum)+":")
            print("li " + int_reg[dest[0]] + ", 1")
            print("_x"+str(labelnum+1)+":")
            labelnum +=2
    elif code['inst_type'] == "FUNCALL":
        print("jal "+ code['dest']['Label'])

    elif code['inst_type'] == "GOTO":
        print("j "+ code['dest']['Label'])

    elif code['inst_type'] == "OR":
        if src1[1] == 'int':
            print("or "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src[1] == 'float':
            print('li $f0, 0')
            print("li " + int_reg[dest[0]] + ", 0")
            print("c.eq.s " + float_reg[src1[0]]+", $f0")
            print("bc1f _x"+ str(labelnum))
            print("c.eq.s " + float_reg[src2[0]]+", $f0")
            print("bc1f _x"+ str(labelnum))
            print("j _x" + str(labelnum+1))
            print("_x"+str(labelnum)+":")
            print("li " + int_reg[dest[0]] + ", 1")
            print("_x"+str(labelnum+1)+":")
            labelnum+=2

    elif code['inst_type'] == "RETURN":
        if dest[1] == 'int':
            print('move $v0, ' + int_reg[dest[0]])
            print('jr $ra')
        elif dest[1] == 'float':
            print('mov.s $f0, ' + float_reg[dest[0]])
            print('jr $ra')

    elif code['inst_type'] == "BREAK":
        print("j "+ code['dest']['Label'])

    elif code['inst_type'] == "CONTINUE":
        print("j "+ code['dest']['Label'])

    elif code['inst_type'] == "PRINT":
        if 'value' in code['dest'].keys():
            temp = "_str" + str(stringnum) + ": .asciiz \"" + code['dest']['value'] + " \n\""
            theStrings.append(temp)
            print("li $v0, 4")
            print("la $a0, _str" + str(stringnum))
            print("syscall")
            stringnum += 1
        elif dest[1] == 'int':
            print("li $v0, 1")
            print("move $a0, " + int_reg[dest[0]])
            print("syscall")
        elif dest[1] == 'float':
            print("li $v0, 2")
            print("mov.s $f12, " + float_reg[dest[0]])
            print("syscall")




# sw r2, 0()
# lw r1, 0(t1) 

# Convert Integer to Float
# mtc1 IntReg, FRsrc
# cvt.s.w FRdest, FRsrc	
# Convert Float to Integer
# cvt.w.s FRdest, FRsrc
# mfc1 IntReg, FRdest    -- YES ALWAYS INT FIRST

def convert(toreg, fromreg): # convert stmt from one type to another
    print('convert')
    if toreg[1] == 'int':
        print('cvt.w.s $f31, ' + float_reg[fromreg[0]])
        print('mfc1 ' + int_reg[toreg[0]] + ' , $f31')
    else:
        print('mtc1 ' + int_reg[fromreg[0]] + ' , $f31')
        print('cvt.w.s ' + float_reg[toreg[0]] + ' , $f31')



def load(reg, var): # just load stmt from addr of var accoridng to type of reg
    print('load')
    if reg[1] == 'int':
        print("addi  $a3, $k0, " + str(reg_to_var['start_addr']))
        print("lw " + int_reg[reg[0]]+ ", 0($a3)")
    else:
        print("addi  $a3, $k0, " + str(freg_to_var['start_addr']))
        print("lw.s " + float_reg[reg[0]]+ ", 0($a3)")
                
    

def store_args(code): # initialize a0, a1 and store args in just before funcall, currmem is in src1 of code
    print('store_args')
    print('li $a0, ' + str(code['src1']))
    print('li $a3, ' + str(code['src1']))
    print('add  $a3, $k0, $a3')
    print('li $a1, ' + str(len(code['src2'])))
    for arg in code['src2']:
        if 'constant' in arg.keys():
            if arg['type'] == 'int':
                print('li $a2, ' + str(arg['constant']))
                print('sw $a2, 0($a3)')
            else:
                print('li.s $f31, ' + str(arg['constant']))
                print('s.s $f31, 0($a3)')
        elif 'tempID' in arg.keys():
            keystr = json.dumps(sorted(arg.items()))
            if arg['type'] == 'int':
                reg = var_to_reg[keystr]
                print('sw ' + int_reg[reg] + ', 0($a3)')
            else:
                reg = var_to_freg[keystr]
                print('s.s ' + float_reg[reg] + ', 0($a3)')
        else: # identifier
            keystr = json.dumps(sorted(arg.items()))
            if arg['type'] == 'int':
                if keystr not in var_to_reg.keys():
                    print("addi  $a2, $k0, " + str(arg['start_addr']))
                    print('lw $a2, 0($a2)')
                    print('sw $a2, 0($a3)')
                else:
                    reg = var_to_reg[keystr]
                    print('sw ' + int_reg[reg] + ', 0($a3)')               
            else:
                if keystr not in var_to_freg.keys():
                    print("addi  $a2, $k0, " + str(arg['start_addr']))
                    print('lw.s $f31, 0($a2)')
                    print('s.s $f31, 0($a3)')
                else:
                    reg = var_to_freg[keystr]
                    print('s.s ' + float_reg[reg] + ', 0($a3)')
        print('addi $a3, $a3, 4')


def load_arg(reg, count): # load from addr a0 + count*4 in funcdef
    print('load_arg')
    if count == 0:
        print('add $a3, $k0, $a0')    
    if reg[1] == 'int':
        print('lw ' + int_reg[reg[0]] + ', 0($a3)')
    else:
        print('lw.s ' + float_reg[reg[0]] + ', 0($a3)')
    print('addi $a3, $a3, 4')


var_modified = {} # variable modified but not stored back, so they need storing back, same structure as var_to_reg
initialise()
print('===== ASSEMBLY ======')
print(len(theCode))
print(len(codeStatus))

for i in range(len(theCode)):
    print(theCode[i])

    if codeStatus[i] == {}:
        if theCode[i]['inst_type'] in ['GOTO', 'EOF', 'BREAK', 'CONTINUE']:
            for var in var_modified.keys():
                spill(var_modified[var])
            getassem(theCode[i], -1, -1, -1)
            for var in var_modified.keys():
                treg_to_var = {}
                tvar_to_reg = {}
                if var_modified[var][1] == 'int':
                    treg_to_var = reg_to_var
                    tvar_to_reg = var_to_reg
                else:
                    treg_to_var = freg_to_var
                    tvar_to_reg = var_to_freg
                treg_to_var[var_modified[var][0]] = {}
                del tvar_to_reg[var]
            var_modified = {}
        elif theCode[i]['inst_type'] == 'FUNCALL':
            store_args(theCode[i])
            for var in var_modified.keys():
                spill(var_modified[var])
            getassem(theCode[i], -1, -1, -1)
            for var in var_modified.keys():
                treg_to_var = {}
                tvar_to_reg = {}
                if var_modified[var][1] == 'int':
                    treg_to_var = reg_to_var
                    tvar_to_reg = var_to_reg
                else:
                    treg_to_var = freg_to_var
                    tvar_to_reg = var_to_freg
                treg_to_var[var_modified[var][0]] = {}
                del tvar_to_reg[var]
            var_to_modified = {}
        else:
            getassem(theCode[i], -1, -1, -1)
        continue
    if theCode[i]['inst_type'] in ['IF0', 'IFEQL', 'IF1']:
        print(var_modified)
        for var in var_modified.keys():
            spill(var_modified[var])
    reg_src = {}
    reg_dest = []
    dest = 'dest'
    print(codeStatus[i])
    for src in ['src1', 'src2']:
        reg_src[src] = []
        if src in codeStatus[i].keys():
            if theCode[i][src]['type'] != 'float':
                tempstr = json.dumps(sorted(theCode[i][src].items()))
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
                    freg_to_var[reg_src[src][0]] = theCode[i][src]
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
            else: # if src is float 
                tempstr = json.dumps(sorted(theCode[i][src].items()))
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
                    reg_to_var[reg_src[src][0]] = theCode[i][src]
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
                        freg_to_var[reg_src[src][0]] = theCode[i][src]

    isDestList = False
    if 'dest' in codeStatus[i].keys():
        if type(codeStatus[i]['dest']) == dict:
            tvar_to_reg = {}
            treg_to_var = {}
            tnum = 0
            tempstr = json.dumps(sorted(theCode[i][dest].items()))
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
                treg_to_var[reg_dest[0]] = theCode[i][dest]
            if 'identifier' in theCode[i][dest].keys():
                
                var_modified[tempstr] = reg_dest
                print("var modified + ", end=" ")
                print(var_modified)
                print("______________________")
        else:
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
                print(result)
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
        print("***********")
        for j in var_to_reg.keys():
            print(j, end="  :  ")
            print(var_to_reg[j])
        print("***********")
        for var in var_modified.keys():
            treg_to_var = {}
            tvar_to_reg = {}
            if var_modified[var][1] == 'int':
                treg_to_var = reg_to_var
                tvar_to_reg = var_to_reg
            else:
                treg_to_var = freg_to_var
                tvar_to_reg = var_to_freg
            treg_to_var[var_modified[var][0]] = {}
            del tvar_to_reg[var]
        var_modified = {}  
    elif i+1 in block_header:
        for var in var_modified.keys():
            treg_to_var = {}
            tvar_to_reg = {}
            if var_modified[var][1] == 'int':
                treg_to_var = reg_to_var
                tvar_to_reg = var_to_reg
            else:
                treg_to_var = freg_to_var
                tvar_to_reg = var_to_freg
            spill(var_modified[var])
            treg_to_var[var_modified[var][0]] = {}
            del tvar_to_reg[var]
        var_modified = {}  


