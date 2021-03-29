.data
list2:  .word   19, 13, 2, 7, 11, 5, 23, 29, 17, 3
size:   .word   10

.globl main
.text

main:
	la      $a0, list2
	lw      $a1, size
	
bubble_sort:
	addi    $t3, $a1, -1									

outer:														
        bge     $zero, $t3, outer_end
        add     $t0, $zero,$zero						    
	    add		$t2,$a0,$zero								

inner:														
        bge     $t0, $t3, inner_end
	
	lw      $t7, 0($t2)										
	lw      $t8, 4($t2)										
	
	ble     $t7, $t8, no_swap
	sw      $t8, 0($t2)
	sw      $t7, 4($t2)
no_swap:	
	addi    $t0, $t0, 1										 
	addi    $t2, $t2, 4
	j       inner
inner_end:
        addi     $t3, $t3, -1								 
        j       outer
outer_end:
	jr      $ra	