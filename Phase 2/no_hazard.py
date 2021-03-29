instructions = [i for i in range(1, 5)]


class Module:
    def __init__(self):
        self.state = False
        self.instruction = 0


# Module Initialization
Id, If, Ex, Mem, Wb = (Module() for _ in range(5))

# Storing in this format for easier access
modules = [If, Id, Ex, Mem, Wb]


# Initializing IF with the first instruction
If.instruction = 1


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

    Wb.state = False
    if (Wb.state == False and Mem.state == False):
        Wb.instruction = Mem.instruction
        Mem.state = False
    if (Mem.state == False and Ex.state == False):
        Mem.instruction = Ex.instruction
        Ex.state = False
    if (Ex.state == False and Id.state == False):
        Ex.instruction = Id.instruction
        Id.state = False
    if (Id.state == False and If.state == False):
        Id.instruction = If.instruction
        If.state = False
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
states = [[(i.state, i.instruction) for i in modules]]

clock = 1  # clock = 1 because we are already initializing with the first state

while (If.instruction or Id.instruction or Ex.instruction or Mem.instruction or Wb.instruction):
    nextState(getNextInstruction(If.instruction))
    states.append([(i.state, i.instruction) for i in modules])
    clock += 1

print(clock)