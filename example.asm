#.globl main 
.text 
main:
	li $t1 , 8
	mtc1 $t1 , $f2
	cvt.s.w $f3 , $f2
	jr $ra
.data
value:	.word 25
Z:	.word 0
