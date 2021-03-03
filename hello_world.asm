.data
hello_world: 
	.asciiz "hello world\n"
.text
.globl main
main:
	li $v0, 4
	la $a0, hello_world
	syscall
	jr $ra
