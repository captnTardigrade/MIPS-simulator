# import re
# from main import *
# from globalVariables import *
# import cache
# import math

# instruction = "lw $s0, 16($s1)"

# args = [i.strip() for i in instruction[2:].split(",")]
# # if "($" in args[1]:
# #     registerPattern = re.compile(r"(\d+)\((\$(\w)(\d+))\)")
# #     match = registerPattern.match(args[1])
# #     src = accessRegister(match.group(2))
# #     if str(src)[:2] == "0x":
# #         modifyRegister(
# #             args[0], memory[int(match.group(1))+int(src, base=16)])
# #     else:
# #         modifyRegister(args[0], src)
# # else:
# #     try:
# #         modifyRegister(args[0], memory[int(data[args[1]], base=16)])
# #     except KeyError:
# #         print("Variable does not exist")
# # pc += 1
# L1 = cache.Cache(16, 256, 4, 2)
# registerPattern = re.compile(r"(\d+)\((\$(\w)(\d+))\)")
# match = registerPattern.match(args[1])
# src = "0x0"
# value = f"{int(match.group(1))+int(src, base=16):012b}"
# print(value)

import globalVariables
import math

blockSize = 2
cacheSize = 8
associativity = 2
accessLatency = 2
level = 1

numBlocks = cacheSize//blockSize
numSets = numBlocks//associativity

block = [None for _ in range(blockSize)]
valid = 0
tag = 0
counter = 0
address = "0"*globalVariables.ADDRESS_BITS
mySet = [[tag, block, valid, counter, address]
         for _ in range(associativity)]
cache = [[[tag, block, valid, counter, address]for _ in range(associativity)] for _ in range(numSets)]

offsetBits = int(math.log2(blockSize))
indexBits = int(math.log2(numSets))
address = globalVariables.ADDRESS_BITS
tagBits = globalVariables.ADDRESS_BITS - indexBits - offsetBits

cache[0][0][1] = "foo"
print(cache[1][0][1])
print(cache[0][0][1])
