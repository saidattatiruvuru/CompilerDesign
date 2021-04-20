.data
_str0: .asciiz "\n "
_str1: .asciiz "th fibonacci: "
_str2: .asciiz "\nYay! "
_str3: .asciiz "\nHurray "
_dataStart: .space 4096
.text 
.globl main 
fibo:
move $a3, $k1
lw $t0, 0($a3)
addi $a3, $a3, 4
li $t1, 0
li $t2, 1
li $t3, 0
sw $t1, 4($k1)
sw $t2, 8($k1)
sw $t3, 12($k1)
j L1
L0:
lw $t0, 4($k1)
move $t1, $t0
lw $t2, 8($k1)
move $t3, $t2
add $t1, $t1 , $t3
move $t4, $t1
li $v0, 4
la $a0, _str0
syscall
li $v0, 1
move $a0, $t4
syscall
move $t0, $t2
move $t2, $t4
sw $t4, 16($k1)
sw $t0, 4($k1)
sw $t2, 8($k1)
L1:
lw $t0, 12($k1)
move $t2, $t0
lw $t4, 0($k1)
move $t1, $t4
slt $t2, $t2 , $t1
beq $t2, $s7, L0
L2:
lw $t0, 8($k1)
move $v0, $t0
jr $ra
jr $ra
jr $ra
main:
la $k0, _dataStart
li $s7, 1
li.s $f29, 1.0
li.s $f30, 0.0
li $v0, 5
syscall
move $t2, $v0
move $t0, $t2
li $k1, 4
add $k1, $k1, $k0
move $a3, $k1
li $a1, 1
sw $t0, 0($a3)
addi $a3, $a3, 4
sw $t0, 0($k0)
jal fibo
lw $t4, 0($k0)
li $v0, 1
move $a0, $t4
syscall
li $v0, 4
la $a0, _str1
syscall
li $v0, 1
move $a0, $t0
syscall
li $v0, 6
syscall
mov.s $f1, $f0
mov.s $f2, $f1
li.s $f3, 0.0
mov.s $f1, $f2
li $t1, 0
cvt.w.s $f31, $f1
mfc1 $t5 , $f31
slt $t2, $t5 , $t1
sw $t0, 4($k0)
sw $t0, 4($k0)
s.s $f2, 8($k0)
s.s $f3, 12($k0)
beq $t2, $s7, L9
j L10
L9:
l.s $f2, 8($k0)
mov.s $f3, $f2
li $t3, -1
cvt.w.s $f31, $f3
mfc1 $t0 , $f31
sgt $t1, $t0 , $t3
li $t1, 1
sub $t1, $t1 , $t1
mov.s $f4, $f2
li $t4, -3
cvt.w.s $f31, $f4
mfc1 $t6 , $f31
slt $t3, $t6 , $t4
li $t3, 1
sub $t3, $t3 , $t3
li $t3, 2
mtc1 $t1 , $f31
cvt.w.s $f5 , $f31
mov.s $f6, $f5
mov.s $f4, $f6
li $t7, 2
cvt.w.s $f31, $f4
mfc1 $t8 , $f31
sgt $t7, $t8 , $t7
cvt.w.s $f31, $f4
mfc1 $t9 , $f31
slt $s0, $t9 , $t7
or $t3, $t7 , $s0
li $t3, 1
sub $t3, $t3 , $t3
s.s $f6, 12($k0)
beq $t3, $s7, L3
j L4
L3:
li $v0, 4
la $a0, _str2
syscall
j L5
L4:
L5:
j L11
L10:
l.s $f2, 8($k0)
mov.s $f6, $f2
li $s0, 1
cvt.w.s $f31, $f6
mfc1 $s1 , $f31
or $t7, $s1 , $s0
li $s0, -2
mtc1 $t7 , $f31
cvt.w.s $f7 , $f31
mov.s $f8, $f7
mov.s $f9, $f8
li $s2, -2
cvt.w.s $f31, $f9
mfc1 $s3 , $f31
sgt $s2, $s3 , $s2
cvt.w.s $f31, $f9
mfc1 $s4 , $f31
slt $s5, $s4 , $s2
or $s0, $s2 , $s5
li $s0, 1
sub $s0, $s0 , $s0
s.s $f8, 12($k0)
beq $s0, $s7, L6
j L7
L6:
li $v0, 4
la $a0, _str3
syscall
j L8
L7:
L8:
L11:
jr $ra
