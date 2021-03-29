# Assembler Directive to load the
# data segment, text segment
	.data
	numOne: .word 7
	numTwo: .word 3
	.text
	.globl main	
main:
	lw $s1, 0($s0)  
	lw $s2, 4($s0)  
	sw $s2, 0($s0)  
	sw $s1, 4($s0)   
	jr $ra