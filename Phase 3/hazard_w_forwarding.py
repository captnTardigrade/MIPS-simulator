import re
from main import instructionSeq, path, caches, _accessRegister
from reading_asm import getInstructions
from globalVariables import *

instructions = []
mainInstructions = getInstructions(path)
for _, i in mainInstructions.items():
    instructions.extend(i)

registers = {instruction: [0 for _ in range(
    10)] for instruction in instructions}

# 0 -> not being used
# 1 -> read
# 2 -> write

for i in instructions:
    loadPattern = re.compile(
        r"lw[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\d*\(\$([a-z][0-9])\)")
    branchPattern = re.compile(
        r"\w{3}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*(\w+)")
    pattern = re.compile(
        r"\w{2,4}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])")
    matches = loadPattern.match(i)
    if matches:
        registers[i][int(matches.group(1)[1:])] = 2
        registers[i][int(matches.group(2)[1:])] = 1

    matches = branchPattern.match(i)
    if matches:
        registers[i][int(matches.group(1)[1:])] = 1
        registers[i][int(matches.group(2)[1:])] = 1

    matches = pattern.match(i)
    if matches:
        registers[i][int(matches.group(1)[1:])] = 2
        registers[i][int(matches.group(2)[1:])] = 1
        registers[i][int(matches.group(3)[1:])] = 1


class Module:
    def __init__(self):
        self.state = False
        self.instruction = None


# Module Initialization
Id, If, Ex, Mem, Wb = (Module() for _ in range(5))

# Storing in this format for easier access
modules = [If, Id, Ex, Mem, Wb]

instructionBuffer = [i for i in instructions]
for _ in range(5):
    instructionBuffer.append(None)


def hasHazard(i1, i2):
    pattern = re.compile(
        r"\w{2,4}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*(.*)")
    loadPattern = re.compile(
        r"lw[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*(.*)")
    matchOne = loadPattern.match(i1)
    matchTwo = pattern.match(i2)
    if matchOne and matchTwo:
        if (matchOne.group(1) == matchTwo.group(2) or matchOne.group(1) == matchTwo.group(3)[1:]):
            return True

    matchOne = loadPattern.match(i1)
    matchTwo = loadPattern.match(i2)

    subRegex = re.compile(r"\d+\(\$(\w\d+)\)")
    matchTwo = subRegex.match(matchTwo.group(2))

    if matchOne and matchTwo:
        if matchOne.group(1) == matchTwo.group(1):
            return True
    for i in range(len(registers[instructions[0]])):
        if i1 and i2:
            if (registers[i1][i] == 1 and registers[i2][i] == 2) or (registers[i1][i] == 2 and registers[i2][i] == 2):
                return True
    return False



_buffer = []
def nextState():
    '''
    Returns: None

    Description:
        Updates the states of modules to the states
        the next clock cycle
    '''
    global modules, _buffer, instructionBuffer
    flag = 0
    Wb.state = False
    if _buffer and Wb.instruction == _buffer[0]:
        _buffer.pop(0)
    
    if (Wb.state == False and Mem.state == True):
        Wb.instruction = Mem.instruction
        Wb.state = True
        Mem.state = False
    if (Mem.state == False and Ex.state == True):
        Mem.instruction = Ex.instruction
        Ex.state = False
        Mem.state = True
    try:
        i = _buffer.index(Id.instruction)
    except ValueError:
        i = 0
    if (i >= 1 and hasHazard(_buffer[i], _buffer[i-1])) or (i >= 2 and hasHazard(_buffer[i], _buffer[i-2])):
        Ex.state = True
        Mem.state = True
    if (Ex.state == False and Id.state == True):
        Ex.instruction = Id.instruction
        Id.state = False
        Ex.state = True
    if (Id.state == False and If.state == True):
        Id.instruction = If.instruction
        If.state = False
        Id.state = True
    if (If.state == False):
        If.state = True
        If.instruction = instructionBuffer.pop(0)
        _buffer.append(If.instruction)

    loadInstruction = re.compile(r"lw[\t ]+\$(\w+)[\t ]*,[\t ]*(\w+)")
    matches = loadInstruction.match(instruction)
    if matches:
        try:
            hexAddress = data[matches.group(2)]
        except KeyError:
            print("Variable does not exist")
            exit(1)
        address = f"{int(hexAddress, base=16):012b}"
        for cache_level in caches:
            if cache_level.isValInCache(address):
                numStalls += cache_level.accessLatency
                cache_level.updateCounter(address)
                break
    loadInstruction = re.compile(r"lw[\t ]+\$(\w+)[\t ]*,[\t ]*(\d+)\((\$\w\d+)\)")
    matches = loadInstruction.match(instruction)
    if matches:
        address = _accessRegister(matches.group(3))
        for cache_level in caches:
            if cache_level.isValInCache(address):
                numStalls += cache_level.accessLatency
                cache_level.updateCounter(address)
                break


states = []
clock = 0
nextState()
states.append([(i.state, i.instruction) for i in modules])
while (If.instruction or Id.instruction or Ex.instruction or Mem.instruction or Wb.instruction):
    nextState()
    states.append([(i.state, i.instruction) for i in modules])
    clock += 1
