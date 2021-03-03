import re
from reading_asm import getData, getInstructions

# Global constants
REGISTER_SIZE = 32
MEMORY_SIZE = 4000

pc = 0
memPointer = 0

registers = [0]*REGISTER_SIZE
memory = [0]*MEMORY_SIZE

path = r"./instructionTest.asm"

'''
d = {"class of register":[indices],"v":[2,3],"s":[17...23]}
R[d["v"][0]]
R[d["s"][0]]
[17, 18, 19, ]
register = "$s7" -> reg[d[register[1]][int(register[-1])]]

'''
namedRegisters = {"r0": 0, "at": 1, "v": [2, 3], "a": [4, 5, 6, 7], "t": [7, 8, 9, 10, 11, 12, 13, 14, 15, 24, 25], "s": [
    16, 17, 18, 19, 20, 21, 22, 23, 30], "k": [26, 27], "gp": 28, "sp": 29, "ra": 31}

data = getData(path)
instructions = getInstructions(path)


# storing variables in memory
for key, value in data.items():
    memory[memPointer] = value
    data[key] = memPointer
    memPointer += 1


def accessRegister(r):
    return registers[namedRegisters[r[1]][int(r[-1])]]


def modifyRegister(r, value):
    registers[namedRegisters[r[1]][int(r[-1])]] = value


def runInstruction(instruction):
    if instruction[:3] == "add":
        args = [i.strip() for i in instruction[3:].split(",")]
        srcOne = accessRegister(args[1])
        try:
            srcTwo = accessRegister(args[2])
        except:
            srcTwo = int(args[2], 16)
        res = srcOne + srcTwo
        modifyRegister(args[0], res)

    elif instruction[:3] == "sub":
        args = [i.strip() for i in instruction[3:].split(",")]
        srcOne = accessRegister(args[1])
        try:
            srcTwo = accessRegister(args[2])
        except:
            srcTwo = int(args[2])
        res = srcOne - srcTwo
        modifyRegister(args[0], res)

    elif instruction[:2] == "lw":
        args = [i.strip() for i in instruction[2:].split(",")]
        src = accessRegister(args[1][2:5])  # contains index of memory
        modifyRegister(args[0], memory[int(args[1][0])//4+src])

def runFile():
    for instruction in instructions["main"]:
        runInstruction(instruction)

runFile()
print(registers)
