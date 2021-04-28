import re
from main import *
from globalVariables import *
import cache
import math

instruction = "lw $s0, 16($s1)"

args = [i.strip() for i in instruction[2:].split(",")]
# if "($" in args[1]:
#     registerPattern = re.compile(r"(\d+)\((\$(\w)(\d+))\)")
#     match = registerPattern.match(args[1])
#     src = accessRegister(match.group(2))
#     if str(src)[:2] == "0x":
#         modifyRegister(
#             args[0], memory[int(match.group(1))+int(src, base=16)])
#     else:
#         modifyRegister(args[0], src)
# else:
#     try:
#         modifyRegister(args[0], memory[int(data[args[1]], base=16)])
#     except KeyError:
#         print("Variable does not exist")
# pc += 1
L1 = cache.Cache(16, 256, 4, 2)
registerPattern = re.compile(r"(\d+)\((\$(\w)(\d+))\)")
match = registerPattern.match(args[1])
src = "0x0"
value = f"{int(match.group(1))+int(src, base=16):012b}"
print(value)
