import sys
sys.path.append("../reading_asm.py")
from reading_asm import getData, getInstructions
import re
# -------------------------PRE-PROCESSING START-------------------------- #
# Global constants
REGISTER_SIZE = 32
MEMORY_SIZE = 4000
BASE = 2000

pc = BASE
memPointer = 0

registers = [0]*REGISTER_SIZE
memory = [0]*MEMORY_SIZE

# path to the asm file
# path = r"{}".format(input("Enter the path to the asm file: "))

'''
namedRegisters design:
    d = {"class of register":[indices],"v":[2,3],"s":[17...23]}
'''
namedRegisters = {"r0": 0, "at": 1, "v": [2, 3], "a": [4, 5, 6, 7], "t": [8, 9, 10, 11, 12, 13, 14, 15, 24, 25], "s": [
    16, 17, 18, 19, 20, 21, 22, 23, 30], "k": [26, 27], "gp": 28, "sp": 29, "ra": 31}

registerStatus = [False for _ in range(REGISTER_SIZE)] # stores True if that register is occupied
moduleStatus = {False: None for _ in range(5)}

data = getData(path)
instructions = getInstructions(path)


# storing variables in memory
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

# -------------------------PRE-PROCESSING END-------------------------- #


def accessRegister(r):
    '''
        fetches the value inside a register
        parameters: (string) name of the register in
        returns: the value of the register
    '''
    if not registerStatus[namedRegisters[r[1:]]]:
        if r == "$zero":
            return 0
        try:
            registerPattern = re.compile(r"\$(\w)(\d+)")
            match = registerPattern.match(r)
            regType = match.group(1)
            regNumber = match.group(2)
            return registers[namedRegisters[regType][int(regNumber)]]
        except:
            try:
                try:
                    return registers[namedRegisters[r]]
                except KeyError:
                    print(f"Unknown reference to a register: {r}")
                    exit(1)
            except KeyError:
                return int(r)
    else:
        return # stall


def modifyRegister(r, value):
    '''
        updates the given register with the given value
        parameters: (string) name of the register, (any) value to be updated with
        returns: None
    '''
    registerPattern = re.compile(r"\$(\w)(\d+)")
    match = registerPattern.match(r)
    regType = match.group(1)
    regNumber = match.group(2)
    try:
        registers[namedRegisters[regType][int(regNumber)]] = value
    except KeyError:
        registers[namedRegisters[r[1:]]] = value


def runInstruction(instruction):
    '''
    runs the given instruction and modifies the global PC accordingly
    parameters: supported assembly instruction
    returns: None
    '''

    global pc
    if pc >= 4000 or pc < 2000:
        return

    if instruction[:4] == "addi":
        
        pc += 1

    elif instruction[:3] == "add":

        pc += 1

    elif instruction[:3] == "sub":
        
        pc += 1

    elif instruction[:2] == "lw":
        
        pc += 1

    elif instruction[:2] == "sw":
        
        pc += 1

    elif instruction[:3] == "bne":
        args = [i.strip() for i in instruction[3:].split(",")]
        if accessRegister(args[0]) != accessRegister(args[1]):
            pc = instructions[args[2]]
            return 
        else:
            pc += 1

    elif instruction[:3] == "beq":
        args = [i.strip() for i in instruction[3:].split(",")]
        if accessRegister(args[0]) == accessRegister(args[1]):
            pc = instructions[args[2]]
            return runInstruction(memory[instructions[args[2]]])
        else:
            pc += 1

    elif instruction[:2] == "jr":
        pc = 3999

    elif instruction[0] == "j":
        pc = instructions[instruction.split()[1].strip()]
        runInstruction(memory[pc])

    elif instruction[:3] == "bge":
        args = [i.strip() for i in instruction[3:].split(",")]
        if int(str(accessRegister(args[0])), 16) >= int(str(accessRegister(args[1])), 16):
            pc = instructions[args[2]]
            return runInstruction(memory[instructions[args[2]]])
        else:
            pc += 1

    elif instruction[:3] == "ble":
        args = [i.strip() for i in instruction[3:].split(",")]
        if int(str(accessRegister(args[0])), 16) <= int(str(accessRegister(args[1])), 16):
            pc = instructions[args[2]]
            return runInstruction(memory[instructions[args[2]]])
        else:
            pc += 1

    elif instruction[:2] == "la":
        args = [i.strip() for i in instruction[2:].split(",")]
        modifyRegister(args[0], data[args[1]])
        pc += 1


def runFile():
    '''
    runs the file at the specified path
    parameters: None
    returns: None
    '''
    global pc
    while memory[pc] != 0:
        runInstruction(memory[pc])


def reinitialize():
    global pc, memPointer, registers, memory, path
    pc = BASE
    memPointer = 0

    registers = [0]*REGISTER_SIZE
    memory = [0]*MEMORY_SIZE

    # path to the asm file
    path = r"{}".format(input("Enter the path to the asm file: "))


def showMemorySegment(start, end):
    '''
    Prints a segment of the memory within the given indices. start is included and end is excluded
    parameters: (int) start, (int) end
    returns: None
    '''
    print(memory[start:end+1])


clock = 0
# while not program done:
#   get the current instruction
#   i = getInstruction()
#   