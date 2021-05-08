import re
import os
from globalVariables import *
import cache
from reading_asm import getData, getInstructions

##---- DEFINE THE LEVELS OF CACHE HERE -----##
L1 = cache.Cache(8, 64, 4, 2, 1)
L2 = cache.Cache(16, 256, 4, 4, 2)
caches = [L1, L2]

def _validRegisterCheck(r):
    errorMessage = f"{r} does not exist"
    if r == "$zero":
        return -1
    registerPattern = re.compile(r"\$(\w)(\d+)")
    match = registerPattern.match(r)
    try:
        if match:
            registers[namedRegisters[match.group(1)][int(match.group(2))]]
            return 2
    except KeyError:
        print(errorMessage)
        exit(1)
    except IndexError:
        print(errorMessage)
        exit(1)
    registerPattern = re.compile(r"\$(\w{2})")
    if registerPattern.match(r):
        try:
            registers[namedRegisters[registerPattern.match(r).group(1)]]
            return 1
        except KeyError:
            print(errorMessage)
            exit(1)
    


def _accessRegister(r):
    '''
        fetches the value inside a register
        parameters: (string) name of the register in
        returns: (str) the value of the register in binary
    '''
    if r == "$zero":
        return 0
    regType = _validRegisterCheck(r)
    if regType == 1:
        registerPattern = re.compile(r"\$(\w{2})")
        return registers[namedRegisters[registerPattern.match(r).group(1)]]
    registerPattern = re.compile(r"\$(\w)(\d+)")
    return registers[namedRegisters[registerPattern.match(r).group(1)][int(registerPattern.match(r).group(2))]]


def _modifyRegister(r, value):
    '''
        updates the given register with the given value in binary
        parameters: (str) name of the register, (str) binary value to be updated with
        returns: None
    '''
    regType = _validRegisterCheck(r)
    if regType == 1:
        registerPattern = re.compile(r"\$(\w{2})")
        registers[namedRegisters[registerPattern.match(r).group(1)]] = value
        return
    registerPattern = re.compile(r"\$(\w)(\d+)")
    registers[namedRegisters[registerPattern.match(r).group(1)][int(registerPattern.match(r).group(2))]] = value





def runInstruction(instruction):
    '''
    runs the given instruction and modifies the global PC accordingly
    parameters: supported assembly instruction
    returns: None
    '''

    global pc
    instructionSeq.append(memory[pc])
    if pc >= MEMORY_SIZE or pc < BASE:
        return

    if instruction[:4] == "addi":
        args = [i.strip() for i in instruction[4:].split(",")]
        if "0x" in args[2]:
            _modifyRegister(args[0], convertToBinary(int(args[2],base=16)+convertToDec(_accessRegister(args[1]))))
        else:
            _modifyRegister(args[0], convertToBinary(int(args[2])+convertToDec(_accessRegister(args[1]))))
        pc += 1

    elif instruction[:3] == "add":
        args = [i.strip() for i in instruction[4:].split(",")]
        srcOne = convertToDec(_accessRegister(args[1]))
        srcTwo = convertToDec(_accessRegister(args[2]))
        res = srcOne + srcTwo
        _modifyRegister(args[0], convertToBinary(res))
        pc += 1

    elif instruction[:3] == "sub":
        args = [i.strip() for i in instruction[4:].split(",")]
        srcOne = convertToDec(_accessRegister(args[1]))
        srcTwo = convertToDec(_accessRegister(args[2]))
        res = srcOne - srcTwo
        _modifyRegister(args[0], convertToBinary(res))
        pc += 1

    elif instruction[:2] == "lw":
        args = [i.strip() for i in instruction[2:].split(",")]
        if "($" in args[1]:
            regPattern = re.compile(r"(\d)+\((\$\w\d+)\)")
            src = _accessRegister(regPattern.match(args[1]).group(2))
            dest = args[0]
            try:
                _modifyRegister(dest, convertToBinary(memory[convertToDec(src)+int(regPattern.match(args[1]).group(1))]))
            except IndexError:
                print("Memory out of bounds")
                exit(1)
        else:
            dest = args[0]
            try:
                _modifyRegister(dest, convertToBinary(memory[int(data[args[1]], base=16)]))
            except KeyError:
                print(f"Variable {args[1]} does not exist")
                exit(1)
            except IndexError:
                print("Memory out of bounds")
                exit(1)
        pc += 1

    elif instruction[:2] == "sw":
        args = [i.strip() for i in instruction[2:].split(",")]
        if "($" in args[1]:
            regPattern = re.compile(r"(\d)+\((\$\w\d+)\)")
            value = _accessRegister(args[0])
            destAddress = convertToDec(_accessRegister(regPattern.match(args[1]).group(2))) + int(regPattern.match(args[1]).group(1))
            try:
                memory[destAddress] = convertToDec(value)
            except IndexError:
                print("Memory out of bounds")
                exit(1)
        else:
            try:
                destAddress = data[args[1]]
                memory[destAddress] = _accessRegister(args[0])
            except KeyError:
                print(f"Variable {args[1]} does not exist")
                exit(1)
            except IndexError:
                print("Memory out of bounds")
                exit(1)
        pc += 1

    elif instruction[:3] == "bne":
        args = [i.strip() for i in instruction[3:].split(",")]
        if _accessRegister(args[0]) != _accessRegister(args[1]):
            pc = instructions[args[2]]
            return runInstruction(memory[instructions[args[2]]])
        else:
            pc += 1

    elif instruction[:3] == "beq":
        args = [i.strip() for i in instruction[3:].split(",")]
        if _accessRegister(args[0]) == _accessRegister(args[1]):
            pc = instructions[args[2]]
            return runInstruction(memory[instructions[args[2]]])
        else:
            pc += 1

    elif instruction[:2] == "jr":
        pc = 4095

    elif instruction[0] == "j":
        pc = instructions[instruction.split()[1].strip()]
        runInstruction(memory[pc])

    elif instruction[:3] == "bge":
        args = [i.strip() for i in instruction[3:].split(",")]
        if convertToDec(_accessRegister(args[0])) >= convertToDec(_accessRegister(args[1])):
            pc = instructions[args[2]]
            return runInstruction(memory[instructions[args[2]]])
        else:
            pc += 1

    elif instruction[:3] == "ble":
        args = [i.strip() for i in instruction[3:].split(",")]
        if convertToDec(_accessRegister(args[0]))<= convertToDec(_accessRegister(args[1])):
            pc = instructions[args[2]]
            return runInstruction(memory[instructions[args[2]]])
        else:
            pc += 1

    elif instruction[:2] == "la":
        args = [i.strip() for i in instruction[2:].split(",")]
        if "($" in args[1]:
            regPattern = re.compile(r"(\d)+\((\$\w\d+)\)")
            src = _accessRegister(regPattern.match(args[1]).group(2))
            dest = args[0]
            try:
                _modifyRegister(dest, convertToBinary(convertToDec(src)+int(regPattern.match(args[1]).group(1))))
            except IndexError:
                print("Memory out of bounds")
                exit(1)
        else:
            dest = args[0]
            try:
                _modifyRegister(dest, convertToBinary(int(data[args[1]], base=16)))
            except KeyError:
                print(f"Variable {args[1]} does not exist")
                exit(1)
            except IndexError:
                print("Memory out of bounds")
                exit(1)
        pc += 1


def runFile():
    '''
    runs the file at the specified path
    parameters: None
    returns: None
    '''
    global pc, instructionSeq
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


def printRegister():

    for x in range(len(namedRegistersList)):

        print(namedRegistersList[x], registers[x])


def printMemory():
    i = 0
    a = 2000
    while i <= memPointer:
        print(a+i, memory[i])
        i = i+INT_SIZE


def showMemorySegment(start, end):
    '''
    Prints a segment of the memory within the given indices. start is included and end is excluded
    parameters: (int) start, (int) end
    returns: None
    '''
    print(memory[start:end+1])


if __name__ == "__main__":
    pass
runFile()

while True:
    print("\nTo reinitialize, enter 1")
    print("To run the file, enter 2")
    print("To show the registers, enter 3")
    print("To show the memory segment, enter 4")
    print("To show the memory segment from given start to end, enter 5")
    print("To exit, press enter any other number")
    command = int(input("Enter the command: "))

    if command == 1:
        reinitialize()
        print("\nReinitialize successful")
    elif command == 2:
        runFile()
        print("\nRun successful")
    elif command == 3:
        print("-----------------------------------REGISTER--------------------------------------")
        printRegister()
    elif command == 4:
        print("-----------------------------------MEMORY----------------------------------------")
        printMemory()
    elif command == 5:
        start, end = map(int, input(
            "Enter start and end indices of the segment to be printed seperated by a space: ").split())
        showMemorySegment(start, end)
    else:
        break

    print("-"*50)
