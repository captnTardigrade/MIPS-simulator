import re
from reading_asm import getData, getInstructions

# Global constants
REGISTER_SIZE = 32
MEMORY_SIZE = 25

BASE = 2000
pc = BASE
memPointer = 0

registers = [0]*REGISTER_SIZE
memory = [0]*4000

path = r"./bubbleSort.asm"

'''
d = {"class of register":[indices],"v":[2,3],"s":[17...23]}
R[d["v"][0]]
R[d["s"][0]]
[17, 18, 19, ]
register = "$s7" -> reg[d[register[1]][int(register[-1])]]

'''
namedRegisters = {"r0": 0, "at": 1, "v": [2, 3], "a": [4, 5, 6, 7], "t": [8, 9, 10, 11, 12, 13, 14, 15, 24, 25], "s": [
    16, 17, 18, 19, 20, 21, 22, 23, 30], "k": [26, 27], "gp": 28, "sp": 29, "ra": 31}

data = getData(path)
instructions = getInstructions(path)


# storing variables in memory
for key, value in data.items():
    if type(value) == list:
        data[key] = hex(memPointer)
        for i in value:
            memory[memPointer] = i
            memPointer += 1
    else:
        memory[memPointer] = value
        data[key] = hex(memPointer)
        memPointer += 1

#storing instructions in memory
instructionPointer = BASE
for label in instructions.keys():
    temp = instructionPointer
    for instruction in instructions[label]:
        memory[instructionPointer] = instruction
        instructionPointer  += 1
    instructions[label] = temp


def accessRegister(r):
    '''
        fetches the value inside a register
    '''
    try:
        registerPattern = re.compile(r"\$(\w)(\d+)")
        match = registerPattern.match(r)
        regType = match.group(1)
        regNumber = match.group(2)
        return registers[namedRegisters[regType][int(regNumber)]]
    except:
        try:
            return registers[namedRegisters[r]]
        except:
            if r == "$zero":
                return 0
            return int(r)
        


def modifyRegister(r, value):
    '''
        updates the given register with the given value
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
    global pc
    if pc >= 4000 or pc < 2000:
        return
    
    if instruction[:4] == "addi":
        args = [i.strip() for i in instruction[4:].split(",")]
        srcOne = accessRegister(args[1])
        if str(srcOne)[:2] == "0x":
            srcOne = int(srcOne, base=16)
        try:
            srcTwo = int(args[2])
        except:
            srcTwo = int(args[2], base=16)
        res = hex(srcOne + srcTwo)
        modifyRegister(args[0], res)

        pc += 1
    
    elif instruction[:3] == "add":
        args = [i.strip() for i in instruction[4:].split(",")]
        srcOne = accessRegister(args[1])
        srcTwo = accessRegister(args[2])
        hexSrcOne = 0
        hexSrcTwo = 0
        res = 0
        if str(srcOne)[:2] == "0x":
            hexSrcOne = int(srcOne, base=16)
        if str(srcTwo)[:2] == "0x":
            hexSrcTwo = int(srcTwo, base=16)
        if (str(srcOne)[:2] == "0x" or str(srcTwo)[:2] == "0x"):
            res = hex(hexSrcOne + hexSrcTwo)
        else:
            res = srcOne + srcTwo
        modifyRegister(args[0], res)

        pc += 1
        
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
    
        pc += 1
    
    elif instruction[:2] == "lw":
        args = [i.strip() for i in instruction[2:].split(",")]
        if "($" in args[1]:
            registerPattern = re.compile(r"(\d+)\((\$(\w)(\d+))\)")
            match = registerPattern.match(args[1])
            src = accessRegister(match.group(2))
            if str(src)[:2] == "0x":
                modifyRegister(args[0], memory[int(match.group(1))//4+int(src, base=16)])
            else:
                modifyRegister(args[0], src)
        else:
            try:
                modifyRegister(args[0], memory[int(data[args[1]], base=16)])            
            except KeyError:
                print("Variable does not exist")
        pc += 1

    elif instruction[:2] == "sw":
        args = [i.strip() for i in instruction[2:].split(",")]
        if "($" in args[1]:
            registerPattern = re.compile(r"(\d+)\((\$(\w)(\d+))\)")
            match = registerPattern.match(args[1])
            src = accessRegister(match.group(2))
            memory[int(match.group(1))//4+int(src, base=16)] = accessRegister(args[0])
        else:
            try:
                memory[int(data[args[1]], base=16)] = accessRegister(args[0])            
            except KeyError:
                print("Variable does not exist")
        pc += 1

    elif instruction[:3] == "bne":
        args = [i.strip() for i in instruction[3:].split(",")]
        if accessRegister(args[0]) != accessRegister(args[1]):
            pc = instructions[args[2]]
            return runInstruction(memory[instructions[args[2]]])
        else:
            pc += 1

    elif instruction[:3] == "beq":
        args = [i.strip() for i in instruction[3:].split(",")]
        if accessRegister(args[0]) == accessRegister(args[1]):
            pc = instructions[args[2]]
            return runInstruction(memory[instructions[args[2]]])
        else:
            pc += 1        
         
    elif instruction.split()[0] == "j":
        for i in instructions[instruction.split()[1]]:
            runInstruction(i)

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

def runFile():
    global pc
    while memory[pc] != 0:
        runInstruction(memory[pc])
        
runFile()
print(memory[:25])