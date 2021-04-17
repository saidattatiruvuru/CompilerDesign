from Parser import *

num_int_reg = 18
num_float_reg = 32
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
    if i in range(10, 18):
        int_reg[i] = "$s" + str(i-10)

for i in range(32):
    float_reg[i] = "$f" + str(i)


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
    print('spill')


def getassem(code, src1, src2, dest): # give assembly code 
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
    elif code['inst_type'] == "SLT":
        if src1[1] == 'int':
            print("slt "+ int_reg[dest[0]] + ", " + int_reg[src1[0]] + " , " + int_reg[src2[0]])
        elif src[1] == 'float':
            print("c.lt.s " + float_reg[])
            print("sub.s  "+ float_reg[dest[0]] + ", " + float_reg[src1[0]] + " , " + float_reg[src2[0]])
    elif code['inst_type'] == "OR":   
            


# sw r2, 0()
# lw r1, 0(t1) 



def convert(toreg, fromreg): # convert stmt from one type to another
    print('convert')

def load(reg, var): # just load stmt from addr of var accoridng to type of reg
    print('load') 

def store_args(code): # initialize a0, a1 and store args in just before funccall, currmem is in src1 of code
    print('store_args')

def load_arg(reg, count): # load from addr a0 + count*4 in funcdef
    print('load_arg')


var_modified = {} # variable modified but not stored back, so they need storing back, same structure as var_to_reg
initialise()
print('===== ASSEMBLY ======')
print(len(theCode))
print(len(codeStatus))

for i in range(len(theCode)):
    print(theCode[i])
    if codeStatus[i] == {}:
        if theCode[i]['inst_type'] == 'GOTO':
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
                tvar_to_reg[tempstr] = {
                    'reg': result[0],
                    'status': codeStatus[i][dest],
                    'isTemp': 'tempID' in theCode[i][dest]
                }                
                treg_to_var[reg_dest[0]] = theCode[i][dest]
            var_modified[tempstr] = reg_dest
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
                reg_dest = [result[0], arg['type']]
                if result[1]:
                    spill(reg_dest)
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

    if theCode[i]['inst_type'] in ['IF0', 'IFEQL', 'IF1']:
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
    
    
    

