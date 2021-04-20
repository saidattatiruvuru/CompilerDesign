.data
_str0: .asciiz "\n "
_str1: .asciiz "\n "
_str2: .asciiz "here   "
_str3: .asciiz "\n "
_wordAlign: .word 0
_dataStart: .space 4096
.text 
.globl main 
main:
la $k0, _dataStart
li $s7, 1
li.s $f29, 1.0
li.s $f30, 0.0
li $t0, 3
li $t1, 7
move $t2, $t0
move $t3, $t1
and $t2, $t2 , $t3
move $t4, $t2
li $v0, 1
move $a0, $t4
syscall
li $v0, 4
la $a0, _str0
syscall
move $t2, $t0
move $t3, $t1
and $t2, $t2 , $t3
sw $t0, 0($k0)
sw $t1, 4($k0)
sw $t4, 8($k0)
bne $t2, $zero, L0
j L1
L0:
lw $t0, 4($k0)
move $t1, $t0
li $v0, 1
move $a0, $t1
syscall
li $v0, 4
la $a0, _str1
syscall
li $v0, 1
move $a0, $t0
syscall
sw $t1, 12($k0)
j L2
L1:
lw $t0, 0($k0)
move $t3, $t0
lw $t1, 4($k0)
move $t4, $t1
or $t3, $t3 , $t4
move $t5, $t3
li $v0, 4
la $a0, _str2
syscall
li $v0, 1
move $a0, $t5
syscall
li $v0, 4
la $a0, _str3
syscall
sw $t5, 12($k0)
L2:
jr $ra
