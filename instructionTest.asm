.data
    numOne: .word 20

    numTwo: 
        .word 10
.text
.globl main
main:
    lw $s1, numOne
    lw $s2, numTwo
    bne $s1, $s2, addThree

foo:
    add $s2, $s2, -10

addThree:
    add $s3, $s1, $s2