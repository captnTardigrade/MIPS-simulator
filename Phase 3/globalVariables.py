from reading_asm import getData, getInstructions
import math

REGISTER_SIZE = 32
MEMORY_SIZE = 4096
BASE = 2000
MEMORY_ACCESS_TIME = 200

ADDRESS_BITS = int(math.log2(MEMORY_SIZE))

pc = BASE
memPointer = 0

registers = [0]*REGISTER_SIZE
memory = [0]*MEMORY_SIZE

instructionSeq = []
# path to the asm file
path = "./add.asm"

'''
namedRegisters design:
    d = {"class of register":[indices],"v":[2,3],"s":[17...23]}
'''
namedRegisters = {"r0": 0, "at": 1, "v": [2, 3], "a": [4, 5, 6, 7], "t": [8, 9, 10, 11, 12, 13, 14, 15, 24, 25], "s": [
    16, 17, 18, 19, 20, 21, 22, 23, 30], "k": [26, 27], "gp": 28, "sp": 29, "ra": 31}

namedRegistersList = ["r0", "at", "v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1", "t2", "t3", "t4", "t5",
                      "t6", "t7", "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9", "k0", "k1", "gp", "sp", "s8", "ra"]

data = getData(path)
instructions = getInstructions(path)

# storing variables in memory
# in the data segment
for key, value in data.items():
    if type(value) == list:
        data[key] = hex(memPointer)
        for i in value:
            memory[memPointer] = i
            memPointer += 4
    else:
        memory[memPointer] = value
        data[key] = hex(memPointer)
        memPointer += 4

# storing instructions in memory
instructionPointer = BASE
for label in instructions.keys():
    temp = instructionPointer
    for instruction in instructions[label]:
        memory[instructionPointer] = instruction
        instructionPointer += 1
    instructions[label] = temp

numCacheHits = 0
totalCacheAccesses = 0