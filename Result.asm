.data
_str0: .asciiz "i:  "
_str1: .asciiz "j:  "
_dataStart: .space 100
.text 
.globl main 
main:
la $k0, _dataStart
li $s7, 1
li.s $f29, 1.0
li.s $f30, 0.0
li $t0, 0
li $t1, 2
li $v0, 5
syscall
move $t2, $v0
move $t3, $t2
sw $t0, 0($k0)
sw $t1, 4($k0)
sw $t3, 8($k0)
j L4
L3:
li $v0, 4
la $a0, _str0
syscall
lw $t0, 0($k0)
li $v0, 1
move $a0, $t0
syscall
move $t1, $t0
li $t3, 2
sgt $t3, $t1 , $t3
slt $t4, $t1 , $t3
or $t1, $t3 , $t4
li $t1, 1
sub $t1, $t1 , $t1
beq $t1, $s7, L0
j L1
L0:
j L4
j L2
L1:
L2:
lw $t0, 4($k0)
move $t3, $t0
lw $t5, 0($k0)
move $t4, $t5
add $t3, $t3 , $t4
move $t0, $t3
move $t4, $t5
li $t6, 1
add $t4, $t4 , $t6
move $t5, $t4
li $v0, 4
la $a0, _str1
syscall
li $v0, 1
move $a0, $t0
syscall
L4:
lw $t0, 0($k0)
move $t2, $t0
lw $t5, 8($k0)
move $t1, $t5
sgt $t2, $t2 , $t1
li $t2, 1
sub $t2, $t2 , $t2
beq $t2, $s7, L3
L5:
jr $ra
