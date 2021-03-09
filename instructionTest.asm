.data
    numOne: .word 10

    numTwo: 
        .word 20
.text
.globl main
main:
    add $s1, 3, 0
    add $s2, 1, 0
foo:
    add $s7, 10, 0
end:
    