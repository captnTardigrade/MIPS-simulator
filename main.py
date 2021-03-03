import re
from reading_asm import getData, getInstructions

# Global constants
REGISTER_SIZE = 32
MEMORY_SIZE = 4000

registers = [0]*REGISTER_SIZE
memory = [0]*MEMORY_SIZE

path = r"./hello_world.asm"

'''
d = {"class of register":[indices],"v":[2,3],"s":[17...23]}
R[d["v"][0]]
R[d["s"][0]]
[17, 18, 19, ]
register = "$s7" -> reg[d[register[1]][int(register[-1])]]

'''
namedRegisters = {"r0": [0], "at": [1], "v": [2, 3], "a": [4, 5, 6, 7], "t": [7, 8, 9, 10, 11, 12, 13, 14, 15, 24, 25], "s": [
    16, 17, 18, 19, 20, 21, 22, 23, 30], "k": [26, 27], "gp": [28], "sp": [29], "ra": [31]}

data = getData(path)
instructions = getInstructions(path)
