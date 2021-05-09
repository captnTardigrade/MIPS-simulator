import re
from main import _accessRegister, instructionSeq, caches, runFile
from reading_asm import getInstructions
from globalVariables import *


runFile()
instructions = []
mainInstructions = getInstructions(path)
for _, i in mainInstructions.items():
    instructions.extend(i)


registers = {instruction: [0 for _ in range(
    len(namedRegistersList))] for instruction in instructions}

# 0 -> not being used
# 1 -> read
# 2 -> write

for i in instructions:
    loadPattern = re.compile(
    r"lw[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*(.*)")
    branchPattern = re.compile(
        r"\w{3}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*(\w+)")
    pattern = re.compile(
        r"\w{2,4}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*(.*)")
    matches = loadPattern.match(i)
    if matches:
        registers[i][int(matches.group(1)[1:])] = 2
        if "$" in matches.group(2):
            temp = re.compile(r"(\d+)\((\$(\w)(\d+|\w+))\)")
            if temp.match(matches.group(2)).group(2) and temp.match(matches.group(2)).group(2) != "$zero":
                registers[i][getRegisterIndex(temp.match(matches.group(2)).group(2))] = 1
    matches = pattern.match(i)
    if matches:
        registers[i][int(matches.group(2)[1:])] = 1
        registers[i][int(matches.group(1)[1:])] = 2
        if "$" in matches.group(3):
            if matches.group(3) != "$zero":
                registers[i][getRegisterIndex(matches.group(3))] = 1
    matches = branchPattern.match(i)
    if matches:
        registers[i][int(matches.group(1)[1:])] = 1
        registers[i][int(matches.group(2)[1:])] = 1

    

class Module:
    def __init__(self):
        self.state = False
        self.instruction = None


# Module Initialization
Id, If, Ex, Mem, Wb = (Module() for _ in range(5))

# Storing in this format for easier access
modules = [If, Id, Ex, Mem, Wb]


# Initializing IF with the first instruction
# If.state = True

instructionBuffer = instructionSeq
for _ in range(5):
    instructionBuffer.append(None)


def hasHazard(i1, i2):
    for i in range(len(registers[instructions[0]])):
        if i1 and i2:
            if (registers[i1][i] == 1 and registers[i2][i] == 2) or (registers[i1][i] == 2 and registers[i2][i] == 2):
                return True
    return False


buffer = []


def nextState():
    '''
    Returns: None

    Description:
        Updates the states of modules to the states
        the next clock cycle
    '''
    global modules, buffer, instructionBuffer, numStalls, numMainMemoryAccesses
    Wb.state = False
    if buffer and Wb.instruction == buffer[0]:
        buffer.pop(0)
    if (Wb.state == False and Mem.state == True):
        Wb.instruction = Mem.instruction
        Wb.state = True
        Mem.state = False
    if (Mem.state == False and Ex.state == True):
        Mem.instruction = Ex.instruction
        Ex.state = False
        Mem.state = True
    try:
        i = buffer.index(Id.instruction)
    except ValueError:
        i = 0
    if (i >= 1 and hasHazard(buffer[i], buffer[i-1])) or (i >= 2 and hasHazard(buffer[i], buffer[i-2])):
        Ex.state = True
        Mem.state = True
    if (Ex.state == False and Id.state == True):
        Ex.instruction = Id.instruction
        Id.state = False
        Ex.state = True
    # if If.instruction and (If.instruction[0] == "b" and (i >= 1 and hasHazard(buffer[i], buffer[i-1])) or (i >= 2 and hasHazard(buffer[i], buffer[i-2]) or (i >= 3 and hasHazard(buffer[i], buffer[i-3])))):

    if (Id.state == False and If.state == True):
        Id.instruction = If.instruction
        If.state = False
        Id.state = True
        # if Id.instruction and (Id.instruction[0] == "b" or (Id.instruction[0] == "j" and Id.instruction != "jr")):
        #     If.state = True
        #     If.instruction = "Stall"
    if (If.state == False):
        If.state = True
        If.instruction = instructionBuffer.pop(0)
        buffer.append(If.instruction)
    
    flagTwo = False
    matchFlag = False
    instruction = Mem.instruction
    if instruction:
        loadInstruction = re.compile(r"lw[ \t]+(\$\w+)[ \t]*,[ \t]*(\d+)\((\$\w+)\)")
        matches = loadInstruction.match(instruction)
        if matches:
            matchFlag = True
            address = _accessRegister(matches.group(3))
            for cache_level in caches:
                numStalls += cache_level.accessLatency - 1
                if cache_level.isValInCache(address):
                    cache_level.updateCounter(address)
                    cache_level.LeastRecentlyUsed(address)
                    flagTwo = True
                    break
        if not matchFlag:
            loadInstruction = re.compile(r"lw[\t ]+\$(\w+)[\t ]*,[\t ]*\$?(\w+)")
            matches = loadInstruction.match(instruction)
            if matches:
                try:
                    hexAddress = data[matches.group(2)]
                except KeyError:
                    print(f"Variable {matches.group(2)} does not exist")
                    exit(1)
                address = f"{int(hexAddress, base=16):012b}"
                for cache_level in caches:
                    numStalls += cache_level.accessLatency - 1
                    if cache_level.isValInCache(address):
                        cache_level.updateCounter(address)
                        cache_level.LeastRecentlyUsed(address)
                        flagTwo = True
                        break
        
        if not flagTwo:
            numMainMemoryAccesses += 1

states = []
nextState()
states.append([(i.state, i.instruction) for i in modules])
clock = 0
while (If.instruction or Id.instruction or Ex.instruction or Mem.instruction or Wb.instruction):
    nextState()
    states.append([(i.state, i.instruction) for i in modules])
    clock += 1