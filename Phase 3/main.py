import re
import os
from globalVariables import *
import cache
from reading_asm import getData, getInstructions

##---- DEFINE THE LEVELS OF CACHE HERE -----##
L1 = cache.Cache(8, 64, 4, 2, 1)
L2 = cache.Cache(16, 256, 4, 4, 2)
caches = [L1, L2]


def accessRegister(r):
    '''
        fetches the value inside a register
        parameters: (string) name of the register in
        returns: the value of the register
    '''
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
        except KeyError:
            return int(r)


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
    instructionSeq.append(memory[pc])
    if pc >= 4000 or pc < 2000:
        return

    if instruction[:4] == "addi":
        args = [i.strip() for i in instruction[4:].split(",")]
        modifyRegister(args[0], accessRegister(args[1]) + int(args[2]))
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
                address = f"{int(match.group(1))+int(src, base=16):012b}"
                flag = 0
                for cache_level in caches:
                    if cache_level.isValInCache(address):
                        modifyRegister(args[0], cache_level.LeastRecentlyUsed(address))
                        flag = 1
                        break
                if not flag:
                    modifyRegister(args[0], memory[int(match.group(1))+int(src, base=16)])
        else:
            try:
                address = f"{int(data[args[1]], base=16):012b}"
                flag = 0
                for cache_level in caches:
                    if cache_level.isValInCache(address):
                        modifyRegister(args[0], cache_level.LeastRecentlyUsed(address))
                        flag = 1
                        break
                if not flag:
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
            memory[int(match.group(1))+int(src, base=16)
                   ] = accessRegister(args[0])
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
# runFile()

# while True:
#     print("\nTo reinitialize, enter 1")
#     print("To run the file, enter 2")
#     print("To show the registers, enter 3")
#     print("To show the memory segment, enter 4")
#     print("To show the memory segment from given start to end, enter 5")
#     print("To exit, press enter any other number")
#     command = int(input("Enter the command: "))

#     if command == 1:
#         reinitialize()
#         print("\nReinitialize successful")
#     elif command == 2:
#         runFile()
#         print("\nRun successful")
#     elif command == 3:
#         print("-----------------------------------REGISTER--------------------------------------")
#         printRegister()
#     elif command == 4:
#         print("-----------------------------------MEMORY----------------------------------------")
#         printMemory()
#     elif command == 5:
#         start, end = map(int, input(
#             "Enter start and end indices of the segment to be printed seperated by a space: ").split())
#         showMemorySegment(start, end)
#     else:
#         break

#     print("-"*50)
