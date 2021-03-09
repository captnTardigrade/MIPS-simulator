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
    if type(value) == list:
        data[key] = memPointer
        for i in value:
            memory[memPointer] = i
            memPointer += 1
    else:
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
        try:
            srcOne = accessRegister(args[1])
        except:
            if (args[1][:2] == "0x"):
                srcOne = int(args[1], base=16)
            else:
                srcOne = int(args[1])
        try:
            srcTwo = accessRegister(args[2])
        except:
            if (args[2][:2] == "0x"):
                srcTwo = int(args[2], base=16)
            else:
                srcTwo = int(args[2])
        res = srcOne + srcTwo
        modifyRegister(args[0], res)

    elif instruction[:3] == "sub":
        args = [i.strip() for i in instruction[3:].split(",")]
        try:
            srcOne = accessRegister(args[1])
        except:
            if (args[1][:2] == "0x"):
                srcOne = int(args[1], base=16)
            else:
                srcOne = int(args[1])
        try:
            srcTwo = accessRegister(args[2])
        except:
            if (args[2][:2] == "0x"):
                srcTwo = int(args[2], base=16)
            else:
                srcTwo = int(args[2])
        res = srcOne + srcTwo
        modifyRegister(args[0], res)
    
    elif instruction[:2] == "lw":
        args = [i.strip() for i in instruction[2:].split(",")]
        if "($" in args[1]:
            src = accessRegister(args[1][-4:-1])  # contains index of memory
            modifyRegister(args[0], memory[int(args[1][:-5])//4+src])
        else:
            try:
                modifyRegister(args[0], memory[data[args[1]]])            
            except KeyError:
                print("Variable does not exist")

    elif instruction[:2] == "sw":
        args = [i.strip() for i in instruction[2:].split(",")]
        if "($" in args[1]:
            src = accessRegister(args[1][-4:-1])  # contains index of memory
            memory[int(args[1][:-5])//4+src] = accessRegister(args[0])
        else:
            try:
                memory[data[args[1]]] = accessRegister(args[0])            
            except KeyError:
                print("Variable does not exist")

    elif instruction[:3] == "bne":
        args = [i.strip() for i in instruction[3:].split(",")]
        if accessRegister(args[0]) != accessRegister(args[1]):
            for i in instructions[args[2]]:
                runInstruction(i)

    elif instruction[:3] == "beq":
        args = [i.strip() for i in instruction[3:].split(",")]
        if accessRegister(args[0]) == accessRegister(args[1]):
            for i in instructions[args[2]]:
                runInstruction(i)

    elif instruction.split()[0] == "j":
        for i in instructions[instruction.split()[1]]:
            runInstruction(i)

def runLabel(label):
    for instruction in instructions[label]:
        runInstruction(instruction)
def runFile():
    for label in instructions.keys():
        runLabel(label)
runFile()
print(registers)