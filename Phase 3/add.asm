.data
numOne: .word 0
numTwo: .word 2
.text
.globl main
main:
    lw $s1, numOne
foo:
    jr $ra