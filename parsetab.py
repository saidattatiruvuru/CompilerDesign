
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND ARITHOP ASSIGN BREAK CHAR CHARACTER COMMENTS CONTINUE ELSE FLOAT FLOATNUM FUNCTION IDENTIFIER IF INPUT INT INTNUM LCB LFB LOG LSB MULTOP NOT OR PRINT RCB RELOP RETURN RFB RSB SEMICOLON SEPARATORS STRING VOID WHILEprgm : prgm stmtprgm : stmt : funcdefstmt : funccall SEMICOLONstmt : declarestmt : assignstmt : ifstmtstmt : whilestmtstmt : printstmtstmt2 : stmt2 stmteltstmt2 : stmtelt : funccall SEMICOLONstmtelt : declarestmtelt : assignstmtelt : ifstmtstmtelt : whilestmtstmtelt : printstmtstmtelt : returnstmtstmtelt : continuestmtstmtelt : breakstmtfuncdef : FUNCTION type IDENTIFIER funcdefy LCB nulltypeargsx RCB LFB stmt2 RFB fundefexitfuncdefy : fundefexit : nulltypeargsx : nulltypeargsnulltypeargs : typeargsnulltypeargs : typeargs : typeargs typeargtypeargs : typeargtypearg : type typeargvaltypeargval : IDENTIFIERexpr : expr OR andtermexpr : andtermandterm : andterm AND equaltermandterm : equaltermequalterm : equalterm LOG reloptermequalterm : reloptermrelopterm : relopterm RELOP arithtermrelopterm : arithtermarithterm : arithterm ARITHOP multermarithterm : multermmulterm : multerm MULTOP singletermmulterm : singletermsingleterm : IDENTIFIERsingleterm : prefix INTNUMsingleterm : prefix FLOATNUMsingleterm : CHARACTERsingleterm : LCB expr RCBsingleterm : arrayidprefix : ARITHOPprefix : assign : lhs ASSIGN rhs SEMICOLONlhs : IDENTIFIERlhs : arrayidrhs : inputstmtrhs : exprrhs : funccallinputstmt : INPUT LCB type RCBfunccall : IDENTIFIER LCB nullargs RCBnullargs : argsnullargs : args : args SEPARATORS argargs : argarg : IDENTIFIERarg : prefix INTNUMarg : prefix FLOATNUMarg : CHARACTERarg : arrayidifstmt  : IF LCB expr RCB LFB ifbegin stmt2 RFB ifend elsepartifbegin : ifend : elsepart : ELSE LFB elsebegin stmt2 RFB elseendelsebegin : elseend : elsepart : whilestmt : WHILE LCB expr RCB LFB whilebegin stmt2 RFB whileendwhilebegin : whileend : printstmt : PRINT LCB printables RCB SEMICOLONprintables : printables SEPARATORS printableprintables : printableprintable : STRINGprintable :  IDENTIFIERprintable : arrayidreturnstmt : RETURN returnelt SEMICOLONreturnelt : exprreturnelt : breakstmt  : BREAK SEMICOLONcontinuestmt : CONTINUE SEMICOLONdeclare : type vars SEMICOLONtype : FLOAT \n  | INT \n  | CHAR vars : var SEPARATORS vars vars : varvar : IDENTIFIER valvar : arrayvararrayvar : arrayvar LSB INTNUM RSBarrayvar : IDENTIFIER LSB INTNUM RSBarrayid : arrayid1arrayid1 : arrayid1 LSB index RSBarrayid1 : IDENTIFIER LSB index RSBindex : INTNUMindex : IDENTIFIERval : ASSIGN exprval : ASSIGN inputstmtval : ASSIGN funccallval : '
    
_lr_action_items = {'FUNCTION':([0,1,2,3,5,6,7,8,9,22,36,90,120,137,151,153,159,160,161,164,168,169,],[-2,10,-1,-3,-5,-6,-7,-8,-9,-4,-89,-51,-78,-70,-77,-74,-75,-23,-68,-21,-73,-71,]),'IDENTIFIER':([0,1,2,3,5,6,7,8,9,11,17,18,19,22,23,28,29,30,31,32,33,34,36,37,40,58,86,90,91,94,95,96,97,98,104,118,119,120,122,128,129,134,135,136,137,138,140,141,142,143,144,145,146,147,148,151,152,153,154,157,158,159,160,161,163,164,165,166,167,168,169,],[-2,12,-1,-3,-5,-6,-7,-8,-9,26,-90,-91,-92,-4,35,42,50,60,70,70,75,50,-89,26,60,70,42,-51,70,70,70,70,70,70,75,-69,-76,-78,131,-11,-11,12,12,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,70,-77,12,-74,-12,-88,-87,-75,-23,-68,-84,-21,-72,-11,12,-73,-71,]),'IF':([0,1,2,3,5,6,7,8,9,22,36,90,118,119,120,128,129,134,135,136,137,138,140,141,142,143,144,145,146,147,151,152,153,154,157,158,159,160,161,163,164,165,166,167,168,169,],[-2,14,-1,-3,-5,-6,-7,-8,-9,-4,-89,-51,-69,-76,-78,-11,-11,14,14,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,-77,14,-74,-12,-88,-87,-75,-23,-68,-84,-21,-72,-11,14,-73,-71,]),'WHILE':([0,1,2,3,5,6,7,8,9,22,36,90,118,119,120,128,129,134,135,136,137,138,140,141,142,143,144,145,146,147,151,152,153,154,157,158,159,160,161,163,164,165,166,167,168,169,],[-2,15,-1,-3,-5,-6,-7,-8,-9,-4,-89,-51,-69,-76,-78,-11,-11,15,15,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,-77,15,-74,-12,-88,-87,-75,-23,-68,-84,-21,-72,-11,15,-73,-71,]),'PRINT':([0,1,2,3,5,6,7,8,9,22,36,90,118,119,120,128,129,134,135,136,137,138,140,141,142,143,144,145,146,147,151,152,153,154,157,158,159,160,161,163,164,165,166,167,168,169,],[-2,16,-1,-3,-5,-6,-7,-8,-9,-4,-89,-51,-69,-76,-78,-11,-11,16,16,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,-77,16,-74,-12,-88,-87,-75,-23,-68,-84,-21,-72,-11,16,-73,-71,]),'FLOAT':([0,1,2,3,5,6,7,8,9,10,22,36,90,92,106,118,119,120,125,126,128,129,130,131,133,134,135,136,137,138,140,141,142,143,144,145,146,147,151,152,153,154,157,158,159,160,161,163,164,165,166,167,168,169,],[-2,17,-1,-3,-5,-6,-7,-8,-9,17,-4,-89,-51,17,17,-69,-76,-78,17,-28,-11,-11,-29,-30,-27,17,17,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,-77,17,-74,-12,-88,-87,-75,-23,-68,-84,-21,-72,-11,17,-73,-71,]),'INT':([0,1,2,3,5,6,7,8,9,10,22,36,90,92,106,118,119,120,125,126,128,129,130,131,133,134,135,136,137,138,140,141,142,143,144,145,146,147,151,152,153,154,157,158,159,160,161,163,164,165,166,167,168,169,],[-2,18,-1,-3,-5,-6,-7,-8,-9,18,-4,-89,-51,18,18,-69,-76,-78,18,-28,-11,-11,-29,-30,-27,18,18,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,-77,18,-74,-12,-88,-87,-75,-23,-68,-84,-21,-72,-11,18,-73,-71,]),'CHAR':([0,1,2,3,5,6,7,8,9,10,22,36,90,92,106,118,119,120,125,126,128,129,130,131,133,134,135,136,137,138,140,141,142,143,144,145,146,147,151,152,153,154,157,158,159,160,161,163,164,165,166,167,168,169,],[-2,19,-1,-3,-5,-6,-7,-8,-9,19,-4,-89,-51,19,19,-69,-76,-78,19,-28,-11,-11,-29,-30,-27,19,19,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,-77,19,-74,-12,-88,-87,-75,-23,-68,-84,-21,-72,-11,19,-73,-71,]),'$end':([0,1,2,3,5,6,7,8,9,22,36,90,120,137,151,153,159,160,161,164,168,169,],[-2,0,-1,-3,-5,-6,-7,-8,-9,-4,-89,-51,-78,-70,-77,-74,-75,-23,-68,-21,-73,-71,]),'SEMICOLON':([4,21,24,25,26,27,38,53,54,55,56,59,60,61,62,63,64,65,67,68,70,79,81,82,83,85,89,99,100,103,105,107,108,110,112,113,114,115,116,117,127,139,148,149,150,155,156,],[22,-99,36,-94,-107,-96,-95,90,-54,-55,-56,-32,-43,-34,-36,-38,-40,-42,-46,-48,-43,-93,-104,-105,-106,-58,-101,-44,-45,120,-100,-98,-97,-31,-47,-33,-35,-37,-39,-41,-57,154,-86,157,158,163,-85,]),'LCB':([12,14,15,16,30,31,32,35,40,57,58,60,78,91,94,95,96,97,98,148,],[28,31,32,33,58,58,58,-22,58,92,58,28,106,58,58,58,58,58,58,58,]),'ASSIGN':([12,13,20,21,26,89,105,],[-52,30,-53,-99,40,-101,-100,]),'LSB':([12,21,26,27,42,60,70,75,89,105,107,108,],[29,34,39,41,29,29,29,29,-101,-100,-98,-97,]),'RCB':([17,18,19,21,28,42,43,44,45,47,48,59,61,62,63,64,65,67,68,69,70,71,72,73,74,75,76,87,88,89,93,99,100,105,106,109,110,111,112,113,114,115,116,117,121,123,124,125,126,130,131,133,],[-90,-91,-92,-99,-60,-63,85,-59,-62,-66,-67,-32,-34,-36,-38,-40,-42,-46,-48,101,-43,102,103,-80,-81,-82,-83,-64,-65,-101,112,-44,-45,-100,-26,-61,-31,127,-47,-33,-35,-37,-39,-41,-79,132,-24,-25,-28,-29,-30,-27,]),'SEPARATORS':([21,25,26,27,38,42,44,45,47,48,59,60,61,62,63,64,65,67,68,70,72,73,74,75,76,81,82,83,85,87,88,89,99,100,105,107,108,109,110,112,113,114,115,116,117,121,127,],[-99,37,-107,-96,-95,-63,86,-62,-66,-67,-32,-43,-34,-36,-38,-40,-42,-46,-48,-43,104,-80,-81,-82,-83,-104,-105,-106,-58,-64,-65,-101,-44,-45,-100,-98,-97,-61,-31,-47,-33,-35,-37,-39,-41,-79,-57,]),'MULTOP':([21,60,64,65,67,68,70,89,99,100,105,112,116,117,],[-99,-43,98,-42,-46,-48,-43,-101,-44,-45,-100,-47,98,-41,]),'ARITHOP':([21,28,30,31,32,40,58,60,63,64,65,67,68,70,86,89,91,94,95,96,97,98,99,100,105,112,115,116,117,148,],[-99,49,49,49,49,49,49,-43,97,-40,-42,-46,-48,-43,49,-101,49,49,49,49,49,49,-44,-45,-100,-47,97,-39,-41,49,]),'RELOP':([21,60,62,63,64,65,67,68,70,89,99,100,105,112,114,115,116,117,],[-99,-43,96,-38,-40,-42,-46,-48,-43,-101,-44,-45,-100,-47,96,-37,-39,-41,]),'LOG':([21,60,61,62,63,64,65,67,68,70,89,99,100,105,112,113,114,115,116,117,],[-99,-43,95,-36,-38,-40,-42,-46,-48,-43,-101,-44,-45,-100,-47,95,-35,-37,-39,-41,]),'AND':([21,59,60,61,62,63,64,65,67,68,70,89,99,100,105,110,112,113,114,115,116,117,],[-99,94,-43,-34,-36,-38,-40,-42,-46,-48,-43,-101,-44,-45,-100,94,-47,-33,-35,-37,-39,-41,]),'OR':([21,55,59,60,61,62,63,64,65,67,68,69,70,71,81,89,93,99,100,105,110,112,113,114,115,116,117,156,],[-99,91,-32,-43,-34,-36,-38,-40,-42,-46,-48,91,-43,91,91,-101,91,-44,-45,-100,-31,-47,-33,-35,-37,-39,-41,91,]),'CHARACTER':([28,30,31,32,40,58,86,91,94,95,96,97,98,148,],[47,67,67,67,67,67,47,67,67,67,67,67,67,67,]),'INTNUM':([28,29,30,31,32,34,39,40,41,46,49,58,66,86,91,94,95,96,97,98,148,],[-50,52,-50,-50,-50,52,80,-50,84,87,-49,-50,99,-50,-50,-50,-50,-50,-50,-50,-50,]),'FLOATNUM':([28,30,31,32,40,46,49,58,66,86,91,94,95,96,97,98,148,],[-50,-50,-50,-50,-50,88,-49,-50,100,-50,-50,-50,-50,-50,-50,-50,-50,]),'INPUT':([30,40,],[57,57,]),'STRING':([33,104,],[74,74,]),'RFB':([36,90,118,119,120,128,129,134,135,136,137,138,140,141,142,143,144,145,146,147,151,152,153,154,157,158,159,161,163,165,166,167,168,169,],[-89,-51,-69,-76,-78,-11,-11,137,151,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,-77,160,-74,-12,-88,-87,-75,-68,-84,-72,-11,168,-73,-71,]),'RETURN':([36,90,118,119,120,128,129,134,135,136,137,138,140,141,142,143,144,145,146,147,151,152,153,154,157,158,159,161,163,165,166,167,168,169,],[-89,-51,-69,-76,-78,-11,-11,148,148,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,-77,148,-74,-12,-88,-87,-75,-68,-84,-72,-11,148,-73,-71,]),'CONTINUE':([36,90,118,119,120,128,129,134,135,136,137,138,140,141,142,143,144,145,146,147,151,152,153,154,157,158,159,161,163,165,166,167,168,169,],[-89,-51,-69,-76,-78,-11,-11,149,149,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,-77,149,-74,-12,-88,-87,-75,-68,-84,-72,-11,149,-73,-71,]),'BREAK':([36,90,118,119,120,128,129,134,135,136,137,138,140,141,142,143,144,145,146,147,151,152,153,154,157,158,159,161,163,165,166,167,168,169,],[-89,-51,-69,-76,-78,-11,-11,150,150,-11,-70,-10,-13,-14,-15,-16,-17,-18,-19,-20,-77,150,-74,-12,-88,-87,-75,-68,-84,-72,-11,150,-73,-71,]),'RSB':([50,51,52,77,80,84,],[-103,89,-102,105,107,108,]),'LFB':([101,102,132,162,],[118,119,136,165,]),'ELSE':([137,153,],[-70,162,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'prgm':([0,],[1,]),'stmt':([1,],[2,]),'funcdef':([1,],[3,]),'funccall':([1,30,40,134,135,152,167,],[4,56,83,139,139,139,139,]),'declare':([1,134,135,152,167,],[5,140,140,140,140,]),'assign':([1,134,135,152,167,],[6,141,141,141,141,]),'ifstmt':([1,134,135,152,167,],[7,142,142,142,142,]),'whilestmt':([1,134,135,152,167,],[8,143,143,143,143,]),'printstmt':([1,134,135,152,167,],[9,144,144,144,144,]),'type':([1,10,92,106,125,134,135,152,167,],[11,23,111,122,122,11,11,11,11,]),'lhs':([1,134,135,152,167,],[13,13,13,13,13,]),'arrayid':([1,28,30,31,32,33,40,58,86,91,94,95,96,97,98,104,134,135,148,152,167,],[20,48,68,68,68,76,68,68,48,68,68,68,68,68,68,76,20,20,68,20,20,]),'arrayid1':([1,28,30,31,32,33,40,58,86,91,94,95,96,97,98,104,134,135,148,152,167,],[21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'vars':([11,37,],[24,79,]),'var':([11,37,],[25,25,]),'arrayvar':([11,37,],[27,27,]),'val':([26,],[38,]),'nullargs':([28,],[43,]),'args':([28,],[44,]),'arg':([28,86,],[45,109,]),'prefix':([28,30,31,32,40,58,86,91,94,95,96,97,98,148,],[46,66,66,66,66,66,46,66,66,66,66,66,66,66,]),'index':([29,34,],[51,77,]),'rhs':([30,],[53,]),'inputstmt':([30,40,],[54,82,]),'expr':([30,31,32,40,58,148,],[55,69,71,81,93,156,]),'andterm':([30,31,32,40,58,91,148,],[59,59,59,59,59,110,59,]),'equalterm':([30,31,32,40,58,91,94,148,],[61,61,61,61,61,61,113,61,]),'relopterm':([30,31,32,40,58,91,94,95,148,],[62,62,62,62,62,62,62,114,62,]),'arithterm':([30,31,32,40,58,91,94,95,96,148,],[63,63,63,63,63,63,63,63,115,63,]),'multerm':([30,31,32,40,58,91,94,95,96,97,148,],[64,64,64,64,64,64,64,64,64,116,64,]),'singleterm':([30,31,32,40,58,91,94,95,96,97,98,148,],[65,65,65,65,65,65,65,65,65,65,117,65,]),'printables':([33,],[72,]),'printable':([33,104,],[73,121,]),'funcdefy':([35,],[78,]),'nulltypeargsx':([106,],[123,]),'nulltypeargs':([106,],[124,]),'typeargs':([106,],[125,]),'typearg':([106,125,],[126,133,]),'ifbegin':([118,],[128,]),'whilebegin':([119,],[129,]),'typeargval':([122,],[130,]),'stmt2':([128,129,136,166,],[134,135,152,167,]),'stmtelt':([134,135,152,167,],[138,138,138,138,]),'returnstmt':([134,135,152,167,],[145,145,145,145,]),'continuestmt':([134,135,152,167,],[146,146,146,146,]),'breakstmt':([134,135,152,167,],[147,147,147,147,]),'ifend':([137,],[153,]),'returnelt':([148,],[155,]),'whileend':([151,],[159,]),'elsepart':([153,],[161,]),'fundefexit':([160,],[164,]),'elsebegin':([165,],[166,]),'elseend':([168,],[169,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> prgm","S'",1,None,None,None),
  ('prgm -> prgm stmt','prgm',2,'p_prgm','Parser.py',173),
  ('prgm -> <empty>','prgm',0,'p_lastprgm','Parser.py',178),
  ('stmt -> funcdef','stmt',1,'p_stmts','Parser.py',181),
  ('stmt -> funccall SEMICOLON','stmt',2,'p_stmt_funccall','Parser.py',184),
  ('stmt -> declare','stmt',1,'p_stmt_declare','Parser.py',187),
  ('stmt -> assign','stmt',1,'p_stmt_assign','Parser.py',190),
  ('stmt -> ifstmt','stmt',1,'p_stmt_ifstmt','Parser.py',193),
  ('stmt -> whilestmt','stmt',1,'p_stmt_whilestmt','Parser.py',196),
  ('stmt -> printstmt','stmt',1,'p_stmt_printstmt','Parser.py',199),
  ('stmt2 -> stmt2 stmtelt','stmt2',2,'p_stmt2','Parser.py',202),
  ('stmt2 -> <empty>','stmt2',0,'p_stmt2_or','Parser.py',207),
  ('stmtelt -> funccall SEMICOLON','stmtelt',2,'p_stmtelt_funccall','Parser.py',210),
  ('stmtelt -> declare','stmtelt',1,'p_stmtelt_declare','Parser.py',213),
  ('stmtelt -> assign','stmtelt',1,'p_stmtelt_assign','Parser.py',216),
  ('stmtelt -> ifstmt','stmtelt',1,'p_stmtelt_ifstmt','Parser.py',219),
  ('stmtelt -> whilestmt','stmtelt',1,'p_stmtelt_whilestmt','Parser.py',222),
  ('stmtelt -> printstmt','stmtelt',1,'p_stmtelt_printstmt','Parser.py',225),
  ('stmtelt -> returnstmt','stmtelt',1,'p_stmtelt_returnstmt','Parser.py',228),
  ('stmtelt -> continuestmt','stmtelt',1,'p_stmtelt_continuestmt','Parser.py',231),
  ('stmtelt -> breakstmt','stmtelt',1,'p_stmtelt_breakstmt','Parser.py',234),
  ('funcdef -> FUNCTION type IDENTIFIER funcdefy LCB nulltypeargsx RCB LFB stmt2 RFB fundefexit','funcdef',11,'p_funcdef','Parser.py',238),
  ('funcdefy -> <empty>','funcdefy',0,'p_fundefy','Parser.py',246),
  ('fundefexit -> <empty>','fundefexit',0,'p_fundefexit','Parser.py',256),
  ('nulltypeargsx -> nulltypeargs','nulltypeargsx',1,'p_nulltypeargsx','Parser.py',264),
  ('nulltypeargs -> typeargs','nulltypeargs',1,'p_nulltypeargs','Parser.py',271),
  ('nulltypeargs -> <empty>','nulltypeargs',0,'p_nulltypeargs_or','Parser.py',275),
  ('typeargs -> typeargs typearg','typeargs',2,'p_typeargs','Parser.py',279),
  ('typeargs -> typearg','typeargs',1,'p_typeargs_or','Parser.py',283),
  ('typearg -> type typeargval','typearg',2,'p_typearg','Parser.py',287),
  ('typeargval -> IDENTIFIER','typeargval',1,'p_typeargval','Parser.py',294),
  ('expr -> expr OR andterm','expr',3,'p_expr','Parser.py',303),
  ('expr -> andterm','expr',1,'p_expr_or','Parser.py',319),
  ('andterm -> andterm AND equalterm','andterm',3,'p_andterm','Parser.py',325),
  ('andterm -> equalterm','andterm',1,'p_andterm_or','Parser.py',341),
  ('equalterm -> equalterm LOG relopterm','equalterm',3,'p_equaltermval','Parser.py',348),
  ('equalterm -> relopterm','equalterm',1,'p_equalterm_or2','Parser.py',366),
  ('relopterm -> relopterm RELOP arithterm','relopterm',3,'p_relopterm','Parser.py',371),
  ('relopterm -> arithterm','relopterm',1,'p_relopterm_or','Parser.py',393),
  ('arithterm -> arithterm ARITHOP multerm','arithterm',3,'p_arithterm','Parser.py',398),
  ('arithterm -> multerm','arithterm',1,'p_arithterm_or','Parser.py',422),
  ('multerm -> multerm MULTOP singleterm','multerm',3,'p_multerm','Parser.py',428),
  ('multerm -> singleterm','multerm',1,'p_multerm_or','Parser.py',461),
  ('singleterm -> IDENTIFIER','singleterm',1,'p_singleterm','Parser.py',478),
  ('singleterm -> prefix INTNUM','singleterm',2,'p_singleterm_or','Parser.py',488),
  ('singleterm -> prefix FLOATNUM','singleterm',2,'p_singleterm_or2','Parser.py',494),
  ('singleterm -> CHARACTER','singleterm',1,'p_singleterm_or3','Parser.py',501),
  ('singleterm -> LCB expr RCB','singleterm',3,'p_singleterm_or4','Parser.py',505),
  ('singleterm -> arrayid','singleterm',1,'p_singleterm_or5','Parser.py',509),
  ('prefix -> ARITHOP','prefix',1,'p_prefix','Parser.py',523),
  ('prefix -> <empty>','prefix',0,'p_prefix_or','Parser.py',527),
  ('assign -> lhs ASSIGN rhs SEMICOLON','assign',4,'p_assign','Parser.py',531),
  ('lhs -> IDENTIFIER','lhs',1,'p_lhs','Parser.py',537),
  ('lhs -> arrayid','lhs',1,'p_lhs_or','Parser.py',546),
  ('rhs -> inputstmt','rhs',1,'p_rhs','Parser.py',555),
  ('rhs -> expr','rhs',1,'p_rhs_or','Parser.py',559),
  ('rhs -> funccall','rhs',1,'p_rhs_or2','Parser.py',563),
  ('inputstmt -> INPUT LCB type RCB','inputstmt',4,'p_inputstmt','Parser.py',568),
  ('funccall -> IDENTIFIER LCB nullargs RCB','funccall',4,'p_funccall','Parser.py',572),
  ('nullargs -> args','nullargs',1,'p_nullargs','Parser.py',586),
  ('nullargs -> <empty>','nullargs',0,'p_nullargs_or','Parser.py',590),
  ('args -> args SEPARATORS arg','args',3,'p_args','Parser.py',594),
  ('args -> arg','args',1,'p_args_or','Parser.py',598),
  ('arg -> IDENTIFIER','arg',1,'p_arg','Parser.py',602),
  ('arg -> prefix INTNUM','arg',2,'p_arg_or','Parser.py',612),
  ('arg -> prefix FLOATNUM','arg',2,'p_arg_or2','Parser.py',618),
  ('arg -> CHARACTER','arg',1,'p_arg_or3','Parser.py',624),
  ('arg -> arrayid','arg',1,'p_arg_or4','Parser.py',628),
  ('ifstmt -> IF LCB expr RCB LFB ifbegin stmt2 RFB ifend elsepart','ifstmt',10,'p_ifstmt','Parser.py',638),
  ('ifbegin -> <empty>','ifbegin',0,'p_ifbegin','Parser.py',641),
  ('ifend -> <empty>','ifend',0,'p_ifend','Parser.py',650),
  ('elsepart -> ELSE LFB elsebegin stmt2 RFB elseend','elsepart',6,'p_elsepart','Parser.py',657),
  ('elsebegin -> <empty>','elsebegin',0,'p_elsebegin','Parser.py',661),
  ('elseend -> <empty>','elseend',0,'p_elseend','Parser.py',670),
  ('elsepart -> <empty>','elsepart',0,'p_elsepart_or','Parser.py',677),
  ('whilestmt -> WHILE LCB expr RCB LFB whilebegin stmt2 RFB whileend','whilestmt',9,'p_whilestmt','Parser.py',680),
  ('whilebegin -> <empty>','whilebegin',0,'p_whilebegin','Parser.py',684),
  ('whileend -> <empty>','whileend',0,'p_whileend','Parser.py',693),
  ('printstmt -> PRINT LCB printables RCB SEMICOLON','printstmt',5,'p_printstmt','Parser.py',700),
  ('printables -> printables SEPARATORS printable','printables',3,'p_printables','Parser.py',704),
  ('printables -> printable','printables',1,'p_printables_or','Parser.py',708),
  ('printable -> STRING','printable',1,'p_printable','Parser.py',712),
  ('printable -> IDENTIFIER','printable',1,'p_printable_or','Parser.py',716),
  ('printable -> arrayid','printable',1,'p_printable_and','Parser.py',725),
  ('returnstmt -> RETURN returnelt SEMICOLON','returnstmt',3,'p_returnstmt','Parser.py',734),
  ('returnelt -> expr','returnelt',1,'p_returnelt','Parser.py',737),
  ('returnelt -> <empty>','returnelt',0,'p_returnelt_or','Parser.py',740),
  ('breakstmt -> BREAK SEMICOLON','breakstmt',2,'p_breakstmt','Parser.py',743),
  ('continuestmt -> CONTINUE SEMICOLON','continuestmt',2,'p_continuestmt','Parser.py',746),
  ('declare -> type vars SEMICOLON','declare',3,'p_declare','Parser.py',749),
  ('type -> FLOAT','type',1,'p_type','Parser.py',775),
  ('type -> INT','type',1,'p_type','Parser.py',776),
  ('type -> CHAR','type',1,'p_type','Parser.py',777),
  ('vars -> var SEPARATORS vars','vars',3,'p_vars','Parser.py',781),
  ('vars -> var','vars',1,'p_lastvars','Parser.py',787),
  ('var -> IDENTIFIER val','var',2,'p_var','Parser.py',792),
  ('var -> arrayvar','var',1,'p_vararray','Parser.py',801),
  ('arrayvar -> arrayvar LSB INTNUM RSB','arrayvar',4,'p_arrayid_var','Parser.py',805),
  ('arrayvar -> IDENTIFIER LSB INTNUM RSB','arrayvar',4,'p_arrayidlast_var','Parser.py',811),
  ('arrayid -> arrayid1','arrayid',1,'p_arrayid','Parser.py',820),
  ('arrayid1 -> arrayid1 LSB index RSB','arrayid1',4,'p_arrayid1','Parser.py',829),
  ('arrayid1 -> IDENTIFIER LSB index RSB','arrayid1',4,'p_arrayidlast','Parser.py',833),
  ('index -> INTNUM','index',1,'p_index','Parser.py',837),
  ('index -> IDENTIFIER','index',1,'p_index1','Parser.py',841),
  ('val -> ASSIGN expr','val',2,'p_val','Parser.py',850),
  ('val -> ASSIGN inputstmt','val',2,'p_val_or','Parser.py',854),
  ('val -> ASSIGN funccall','val',2,'p_val_or2','Parser.py',858),
  ('val -> <empty>','val',0,'p_emptyval','Parser.py',862),
]
