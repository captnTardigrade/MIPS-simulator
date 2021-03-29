import re
import itertools

instructions = ["lw $r1, 0($r2)", "sub $r4, $r1, $r5",
                "and $r6, $r1, $r7"]

registers = [[0 for _ in range(10)] for _ in instructions]

# 0 -> not being used
# 1 -> read
# 2 -> write

for i in range(len(instructions)):
    loadPattern = re.compile(
        r"lw[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\d*\(\$([a-z][0-9])\)")
    pattern = re.compile(
        r"\w{2,3}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])")
    matches = loadPattern.match(instructions[i])
    if matches:
        registers[i][int(matches.group(1)[1:])] = 2
        registers[i][int(matches.group(2)[1:])] = 1

    matches = pattern.match(instructions[i])
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
If.instruction = instructions[0]
If.state = True


instructionBuffer = [i for i in instructions]
buffer = []

def nextState():
    '''
    Input: nextInstruction (string)

    Returns: None

    Description:
        Updates the states of modules to the states
        the next clock cycle
    '''
    global modules, buffer
    Wb.state = False
    if (Wb.state == False and Mem.state == True):
        Wb.instruction = Mem.instruction
        Wb.state = True
        Mem.state = False
    if (Mem.state == False and Ex.state == True):
        Mem.instruction = Ex.instruction
        Ex.state = False
        Mem.state = True
    flag = 0
    i = 0
    try:
        i = buffer.index(Id.instruction)
    except ValueError:
        pass
    if i >= 1:
        for j in range(len(registers[0])):
            if (registers[i][j] == 2 and registers[i-1][j] == 2) or (registers[i][j] == 2 and registers[i-2][j] == 2) or (registers[i][j] == 1 and registers[i-1][j] == 2) or (registers[i][j] == 1 and registers[i-2][j] == 2):
                flag = 1
                break
    if flag:
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
        if instructionBuffer:
            If.instruction = instructionBuffer.pop(0)
        buffer.append(If.instruction)


# Stores the states of modules in each state
# states = [[(i.state, i.instruction) for i in modules]]
states = []

clock = 0

while (instructionBuffer):
    states.append([(i.state, i.instruction) for i in modules])
    nextState()
    clock += 1

print(clock)
for state in states:
    print(state)
