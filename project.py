import collections
command = input()
reg = [1, 2, 3]
mem = [0, 1, 2, 3, 4]

# add $r1, $r2, $r3
# 
# instruction = ["add", "$r1", "$r2", "$r3"]
# command[:3], command[3:].split(',')


def arithmatic(command):
    instruction = command[3:].split(',')
    if command[:3] == "add":
        dest = int(instruction[0][-1])
        num1 = int(instruction[1][-1])
        num2 = int(instruction[2][-1])
        reg[dest-1] = reg[num1-1] + reg[num2-1]
    elif command[:3] == "sub":
        dest = int(instruction[0][-1])
        num1 = int(instruction[1][-1])
        num2 = int(instruction[2][-1])
        reg[dest-1] = reg[num1-1] - reg[num2-1]


# $s2 = "mem[i]"
# lw  $s1,1($s2)
# 1($s2) -> mem[i+1]
# a,v,t,r
# $v0, 4
# syscall

# instructionSet = [I1, I2, I3]
# jump I1
# currentI = 0
# while currentI < len(instrctionSet):
#     execute(currentI)
#     # jump I1
#     # execute(instructionSet["end"])
#     currentI += 1

# 1. pattern matching/splitting
# 2. different types of registers in MIPS
# 3. storing instructions in dictionary -> reading .asm files and using them
# 4. error handling
# 5. limit on size of arrays and limiting the integer result values
# [Optional] 6. autocomplete
# 7. PC program counter implementation
# 8. step-by-step
# 9. pseudo instructions

# d = {"class of register":[indices],"v":[2,3],"s":[17...23]}
# R[d["v"][0]]
# R[d["s"][0]]
# [17, 18, 19, ]
# register = "$s7" -> reg[d[register[1]][int(register[-1])]]



