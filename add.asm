.data
numOne: .word 10
numTwo: .word 20
.text
main:
    addi $s0, $s0, 0x0
    lw $s1, 0($s0)
    lw $s2, 4($s0)
    add $s3, $s1, $s2
    jr $ra
foo:
    jr $ra