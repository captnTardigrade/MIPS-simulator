instructions = [i for i in range(1, 5)]


def getNextInstruction(previousInstruction):
    global instructions
    if previousInstruction and previousInstruction < len(instructions):
        return instructions[previousInstruction]
    return None

class Module:
    def __init__(self):
        self.state = False
        self.instruction = 0

Id = Module()
If = Module()
Ex = Module()
Mem = Module()
Wb = Module()

modules = [Id, If, Ex, Mem, Wb]

If.instruction = 1

def nextState(nextInstruction):
    Wb.state=False
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
    if(If.state==False):
        If.instruction = nextInstruction

def printStates():
    print("-"*40)
    print(f"IF:  {If.state} {If.instruction}")
    print(f"ID:  {Id.state} {Id.instruction}")
    print(f"EX:  {Ex.state} {Ex.instruction}")
    print(f"MEM: {Mem.state} {Mem.instruction}")
    print(f"WB:  {Wb.state} {Wb.instruction}")
    print("-"*40)

clock = 1
while (If.instruction or Id.instruction or Ex.instruction or Mem.instruction or Wb.instruction):
    nextState(getNextInstruction(If.instruction))
    clock += 1

print(clock)