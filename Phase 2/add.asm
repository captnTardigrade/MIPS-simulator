.data
numOne: .word 0
numTwo: .word 2
.text
.globl main
main:
    lw $s1, numOne
    lw $s2, numTwo
loop:
    beq $s1, $s2, foo
    addi $s1, $s1, 1
    j loop
foo:
    jr $ra