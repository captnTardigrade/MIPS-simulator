import re
from globalVariables import *
from main import caches, _accessRegister



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


def getNextInstruction(previousInstruction):
    '''
    Input: Previous instruction
    Returns: The next instruction if it's available, else returns None
    '''
    global instructions
    if previousInstruction and previousInstruction < len(instructions):
        return instructions[previousInstruction]
    return None


def nextState(nextInstruction):
    '''
    Input: nextInstruction (string)

    Returns: None

    Description:
        Updates the states of modules to the states
        the next clock cycle
    '''
    global modules
    Wb.state = False
    if (Wb.state == False and Mem.state == True):
        Wb.instruction = Mem.instruction
        Wb.state = True
        Mem.state = False
    if (Mem.state == False and Ex.state == True):
        Mem.instruction = Ex.instruction
        Ex.state = False
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
        If.instruction = nextInstruction
        If.state = True

    flagTwo = False
    instruction = Mem.instruction
    if instruction:
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
                    flagTwo = True
                    break
        loadInstruction = re.compile(r"lw[\t ]+\$(\w+)[\t ]*,[\t ]*(\d+)\((\$\w\d+)\)")
        matches = loadInstruction.match(instruction)
        if matches:
            address = _accessRegister(matches.group(3))
            for cache_level in caches:
                if cache_level.isValInCache(address):
                    numStalls += cache_level.accessLatency
                    cache_level.updateCounter(address)
                    flagTwo = True
                    break
        if not flagTwo:
            numMainMemoryAccesses += 1


def printStates():
    print("-"*40)
    print(f"IF:  {If.state} {If.instruction}")
    print(f"ID:  {Id.state} {Id.instruction}")
    print(f"EX:  {Ex.state} {Ex.instruction}")
    print(f"MEM: {Mem.state} {Mem.instruction}")
    print(f"WB:  {Wb.state} {Wb.instruction}")
    print("-"*40)


# Stores the states of modules in each state
states = [tuple(i.instruction for i in modules)]

clock = 0

while (If.instruction or Id.instruction or Ex.instruction or Mem.instruction or Wb.instruction):
    nextState(getNextInstruction(If.instruction))
    states.append(tuple(i.instruction for i in modules))
    clock += 1

print(numMainMemoryAccesses)