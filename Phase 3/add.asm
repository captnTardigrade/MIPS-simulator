.data
array: 
	.word 12, 34, 67, 1, 45, 90, 11, 33, 67, 19
.text
.globl main
main:
	lw $s1  , 0($s0)
	add $s3, $s1, $s2
	lw $s1, numOne