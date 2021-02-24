.data
hello_world:
	.asciiz "hello world\n"

.text
.globl main
main:
	li $v0, 4           	#load appropriate system call code into register $v0; code for printing string is 4
	la $a0, hello_world 	#load address of string to be printed into $a0
	syscall
	jr $ra
