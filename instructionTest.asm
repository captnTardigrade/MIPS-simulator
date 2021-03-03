.data
    numOne: .word 10

    numTwo: 
        .word 20
.text
.globl main
main:
    lw $s1, 0($s0)
    lw $s2, 4($s0)
    add $s3, $s1, $s2
    jr $ra