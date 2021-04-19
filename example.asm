#.globl main 
.text 
func:	
	add $t4, $t2, $t3	
	sub $t5, $t2, $t3
	move $a0, $t1
	li $v0, 1  
	syscall	
	jr $ra
main:
	li $t1 , 8
	jal func
	move $a0, $t1
	li $v0, 1  
	syscall	
	jr $ra
.data
value:	.word 25
Z:	.word 0
