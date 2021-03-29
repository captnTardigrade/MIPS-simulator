import re

instructions = ["lw $r1, 0($r2)", "sub $r3, $r1, $r4"]

registers = {f"r{i}": False for i in range(1,5)}

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


def getNextInstruction(previousInstruction):
    '''
    Input: Previous instruction
    Returns: The next instruction if it's available, else returns None
    '''
    global instructions
    i = instructions.index(previousInstruction)
    print(i)
    if i:
        return instructions[i]
    return None


def nextState(nextInstruction):
    '''
    Input: nextInstruction (string)

    Returns: None

    Description:
        Updates the states of modules to the states
        the next clock cycle
    '''
    currentInstruction = If.instruction
    loadOrStorePattern = re.compile(r"[lsw]{2}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\d*\(\$([a-z][0-9])\)")
    matches = loadOrStorePattern.match(currentInstruction)



    if (Wb.state == False and Mem.state == False):
        Wb.instruction = Mem.instruction
    if (Mem.state == False and Ex.state == False):
        # if register being access is yet to be updated:
        #     Mem.state = True
        #     Ex.state = True
        Mem.instruction = Ex.instruction
    if (Ex.state == False and Id.state == False):
        Ex.instruction = Id.instruction
    if (Id.state == False and If.state == False):
        Id.instruction = If.instruction
    if(If.state == False):
        If.instruction = nextInstruction


def printStates():
    print("-"*40)
    print(f"IF:  {If.state} {If.instruction}")
    print(f"ID:  {Id.state} {Id.instruction}")
    print(f"EX:  {Ex.state} {Ex.instruction}")
    print(f"MEM: {Mem.state} {Mem.instruction}")
    print(f"WB:  {Wb.state} {Wb.instruction}")
    print("-"*40)


# Stores the states of modules in each state
# states = [[(i.state, i.instruction) for i in modules]]
states = []

clock = 0

while (If.instruction or Id.instruction or Ex.instruction or Mem.instruction or Wb.instruction):
    states.append([(i.state, i.instruction) for i in modules])
    nextState(getNextInstruction(If.instruction))
    clock += 1

print(clock)