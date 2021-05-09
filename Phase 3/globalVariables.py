from reading_asm import getData, getInstructions
import math
import re

REGISTER_SIZE = 32
MEMORY_SIZE = 4096
BASE = 2000
MEMORY_ACCESS_TIME = 200

INT_SIZE = 4

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
typeDef = {}
instructions = getInstructions(path)

# storing variables in memory
# in the data segment
for key, value in data.items():
    data[key] = hex(memPointer)
    if type(value) == list:
        typeDef[key] = type(value).__name__
        for i in value:
            memory[memPointer] = i
            memPointer += INT_SIZE
    else:
        memory[memPointer] = value
        typeDef[key] = type(value).__name__
        memPointer += INT_SIZE

# storing instructions in memory
instructionPointer = BASE
for label in instructions.keys():
    temp = instructionPointer
    for instruction in instructions[label]:
        memory[instructionPointer] = instruction
        instructionPointer += 1
    instructions[label] = temp

numMainMemoryAccesses = 0
numStalls = 0

def convertToBinary(i):
    return f"{i:032b}"

def convertToDec(i):
    return int(str(i), base=2)

def getRegisterIndex(reg):
    '''
    parameters: (str) register in the format "$<registerName>"
    returns: (int) if the register exists
            otherwise exits the program
    '''
    errorMessage = f"Unknown register {reg}"
    pattern = re.compile(r"\$(\w)(\d+)")
    match = pattern.match(reg)
    if match:
        try:
            return namedRegisters[match.group(1)][int(match.group(2))]
        except KeyError:
            print(errorMessage)
            exit(1)
        except IndexError:
            print(errorMessage)
            exit(1)
    else:
        pattern = re.compile(r"\$(\w{2})")
        match = pattern.match(reg)
        if not match:
            print(errorMessage)
            exit(1)
        try:
            return namedRegisters[match.group(1)]
        except KeyError:
            print(errorMessage)
            exit(1)

