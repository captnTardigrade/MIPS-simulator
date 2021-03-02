.data
hello_world: 
	.asciiz "hello world\n"
num: .word 7
.text
.globl main
main:
	li $v0, 4
	la $a0, hello_world
	syscall
	jr $ra
