.data
_str0: .asciiz "Array values "
_str1: .asciiz "  "
_str2: .asciiz "\n "
_dataStart: .space 4096
.text 
.globl main 
main:
la $k0, _dataStart
li $s7, 1
li.s $f29, 1.0
li.s $f30, 0.0
li $t0, 0
li $v0, 5
syscall
move $t1, $v0
move $t2, $t1
sw $t0, 44($k0)
sw $t2, 0($k0)
j L3
L2:
li $t0, 4
li $t2, 0
li $t3, 10
lw $t4, 44($k0)
sgt $t5, $t4 , $t3
beqz $t5, L1
L1:
lw $t4, 44($k0)
mul $t5, $t0 , $t4
add $t2, $t5 , $t2
mul $t0, $t0 , $t3
li $t3, 4
add $t6, $t2 , $t3
li $v0, 5
syscall
move $t0, $v0
add $t6, $k0 , $t6
sw $t0, 0($t6)
move $t5, $t4
li $t2, 1
add $t5, $t5 , $t2
move $t4, $t5
sw $t4, 44($k0)
L3:
lw $t4, 44($k0)
move $t7, $t4
lw $t8, 0($k0)
move $t9, $t8
slt $t7, $t7 , $t9
beq $t7, $s7, L2
L4:
li $t4, 0
li $t8, 0
sw $t4, 48($k0)
sw $t8, 52($k0)
j L24
L23:
lw $t4, 48($k0)
move $t3, $t4
li $t8, 1
add $t3, $t3 , $t8
move $s0, $t3
sw $s0, 52($k0)
j L21
L20:
slt $t4, $t4 , $s0
beq $t4, $s7, L17
j L18
L17:
move $s1, $s0
li $s2, 4
li $s3, 0
li $s4, 10
lw $s5, 48($k0)
sgt $s6, $s5 , $s4
sw $s1, 56($k0)
beqz $s6, L12
L12:
lw $s1, 48($k0)
mul $s6, $s2 , $s1
add $s3, $s6 , $s3
mul $s2, $s2 , $s4
li $s4, 4
add $s0, $s3 , $s4
add $s0, $k0 , $s0
sw $s6, 0($s0)
li $s5, 4
li $t0, 0
li $t0, 10
lw $t1, 52($k0)
sgt $t0, $t1 , $t0
beqz $t0, L16
L16:
lw $t1, 52($k0)
mul $t0, $s5 , $t1
add $s1, $t0 , $s1
mul $s5, $s5 , $t0
li $t0, 4
add $s4, $s1 , $t0
lw $t0, 56($k0)
add $s4, $k0 , $s4
sw $t0, 0($s4)
j L19
L18:
L19:
lw $t0, 52($k0)
move $t1, $t0
li $s0, 1
add $t1, $t1 , $s0
move $t0, $t1
sw $t0, 52($k0)
L21:
lw $t0, 52($k0)
move $t8, $t0
lw $t1, 0($k0)
move $t2, $t1
slt $t8, $t8 , $t2
beq $t8, $s7, L20
L22:
lw $t0, 48($k0)
move $s0, $t0
li $s2, 1
add $s0, $s0 , $s2
move $t0, $s0
sw $t0, 48($k0)
L24:
lw $t0, 48($k0)
move $t1, $t0
lw $t2, 0($k0)
move $t3, $t2
slt $t1, $t1 , $t3
beq $t1, $s7, L23
L25:
li $t0, 0
sw $t0, 44($k0)
j L29
L28:
li $v0, 4
la $a0, _str0
syscall
lw $t0, 44($k0)
li $v0, 1
move $a0, $t0
syscall
li $v0, 4
la $a0, _str1
syscall
li $s4, 4
li $t2, 0
li $s1, 10
sgt $s5, $t0 , $s1
beqz $s5, L27

L27:
lw $t0, 44($k0)
mul $s5, $s4 , $t0
add $t2, $s5 , $t2
mul $s4, $s4 , $s1
addi  $a3, $k0 , 4
add  $a3, $a3 , $t2
lw $s3, 0($a3)
li $v0, 1
move $a0, $s3
syscall
li $v0, 4
la $a0, _str2
syscall
move $s4, $t0
li $s5, 1
add $s4, $s4 , $s5
move $t0, $s4
sw $t0, 44($k0)
L29:
lw $t0, 44($k0)
move $s2, $t0
lw $t1, 0($k0)
move $s6, $t1
slt $s2, $s2 , $s6
beq $s2, $s7, L28
L30:
jr $ra