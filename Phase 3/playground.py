import re
from globalVariables import data, memory
from main import caches, _accessRegister

numStalls = 0

instruction = "lw $r1 , 12($r12)"
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