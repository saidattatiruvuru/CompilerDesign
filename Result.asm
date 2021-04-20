.data
_str0: .asciiz "f1 [10.5]  :  "
_str1: .asciiz "\n "
_str2: .asciiz "i1 [10] :  "
_str3: .asciiz "\n "
_str4: .asciiz "c [9] :  "
_str5: .asciiz "\n "
_str6: .asciiz "i ==3 : continued\n "
_str7: .asciiz "i && f [1]:  "
_str8: .asciiz "\n "
_str9: .asciiz "i:  "
_str10: .asciiz "\n "
_str11: .asciiz "i [1] :  "
_str12: .asciiz "\n "
_strerror: .asciiz " ERROR! "
_wordAlign: .word 0
_dataStart: .space 4096
.text 
.globl main 
main:
la $k0, _dataStart
li $s7, 1
li.s $f29, 1.0
li.s $f30, 0.0
li.s $f1, 5.5
li $t0, 5
move $t1, $t0
mov.s $f2, $f1
mtc1 $t1 , $f31
cvt.s.w $f3 , $f31
add.s  $f4, $f3 , $f2
mov.s $f5, $f4
li $v0, 4
la $a0, _str0
syscall
li $v0, 2
mov.s $f12, $f5
syscall
li $v0, 4
la $a0, _str1
syscall
move $t1, $t0
mov.s $f2, $f1
mtc1 $t1 , $f31
cvt.s.w $f6 , $f31
add.s  $f4, $f6 , $f2
cvt.w.s $f31, $f4
mfc1 $t2 , $f31
move $t3, $t2
li $v0, 4
la $a0, _str2
syscall
li $v0, 1
move $a0, $t3
syscall
li $v0, 4
la $a0, _str3
syscall
li.s $f4, 4.5
move $t4, $t0
mtc1 $t4 , $f31
cvt.s.w $f7 , $f31
add.s  $f4, $f4 , $f7
cvt.w.s $f31, $f4
mfc1 $t5 , $f31
move $t6, $t5
li $v0, 4
la $a0, _str4
syscall
li $v0, 1
move $a0, $t6
syscall
li $v0, 4
la $a0, _str5
syscall
s.s $f1, 0($k0)
sw $t0, 4($k0)
s.s $f5, 8($k0)
sw $t3, 12($k0)
sw $t6, 16($k0)
j L7
L6:
lw $t0, 4($k0)
move $t4, $t0
li $t3, 1
sub $t4, $t4 , $t3
move $t0, $t4
move $t3, $t0
li $t6, 3
sgt $t7, $t3 , $t6
slt $t8, $t3 , $t6
li $t3, 0
bnez $t7, _x0
bnez $t8, _x0
j _x1
_x0:
li $t3, 1
_x1:
sub $t3, $s7 , $t3
sw $t0, 4($k0)
bne $t3, $zero, L0
j L1
L0:
li $v0, 4
la $a0, _str6
syscall
j L7
j L2
L1:
L2:
lw $t0, 4($k0)
move $t6, $t0
li $t7, 1
sgt $t8, $t6 , $t7
slt $t9, $t6 , $t7
li $t6, 0
bnez $t8, _x2
bnez $t9, _x2
j _x3
_x2:
li $t6, 1
_x3:
sub $t6, $s7 , $t6
bne $t6, $zero, L3
j L4
L3:
lw $t0, 4($k0)
move $t7, $t0
l.s $f1, 0($k0)
mov.s $f5, $f1
cvt.w.s $f31, $f5
mfc1 $s0 , $f31
li $t7, 1
beqz $t7, _x4
beqz $s0, _x4
j _x5
_x4:
li $t7, 0
_x5:
move $s1, $t7
li $v0, 4
la $a0, _str7
syscall
li $v0, 1
move $a0, $s1
syscall
li $v0, 4
la $a0, _str8
syscall
sw $s1, 20($k0)
j L8
j L5
L4:
L5:
li $v0, 4
la $a0, _str9
syscall
lw $t0, 4($k0)
li $v0, 1
move $a0, $t0
syscall
li $v0, 4
la $a0, _str10
syscall
L7:
lw $t0, 4($k0)
move $t1, $t0
l.s $f1, 0($k0)
mov.s $f2, $f1
cvt.w.s $f31, $f2
mfc1 $s1 , $f31
li $t1, 1
beqz $t1, _x6
beqz $s1, _x6
j _x7
_x6:
li $t1, 0
_x7:
bne $t1, $zero, L6
L8:
li $v0, 4
la $a0, _str11
syscall
lw $t0, 4($k0)
li $v0, 1
move $a0, $t0
syscall
li $v0, 4
la $a0, _str12
syscall
jr $ra
_error:
li $v0, 4
la $a0, _strerror
syscall
li $v0, 10
syscall
