import re
from main import instructionSeq, path
from reading_asm import getInstructions

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


# Initializing IF with the first instruction
# If.state = True


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
        if (matchOne.group(1) == matchTwo.group(2)  or matchOne.group(1) == matchTwo.group(3)[1:]):
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


buffer = []


def nextState():
    '''
    Returns: None

    Description:
        Updates the states of modules to the states
        the next clock cycle
    '''
    global modules, buffer, instructionBuffer
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
    if (Id.state == False and If.state == True):
        Id.instruction = If.instruction
        If.state = False
        Id.state = True
    if (If.state == False):
        If.state = True
        If.instruction = instructionBuffer.pop(0)
        buffer.append(If.instruction)


states = []
clock = 0
nextState()
states.append([(i.state, i.instruction) for i in modules])
while (If.instruction or Id.instruction or Ex.instruction or Mem.instruction or Wb.instruction):
    nextState()
    states.append([(i.state, i.instruction) for i in modules])
    clock += 1
