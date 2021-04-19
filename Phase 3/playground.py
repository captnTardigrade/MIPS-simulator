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
        r"lw[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*(.*)")
    branchPattern = re.compile(
        r"\w{3}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*(\w+)")
    pattern = re.compile(
        r"\w{2,4}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*(.*)")
    arithmeticPattern = re.compile(
        r"\w{2,3}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])")
    arithmeticImmediatePattern = re.compile(
        r"\w{3,4}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\d+")
    matches = loadPattern.match(i)
    if matches:
        registers[i][int(matches.group(1)[1:])] = 2
        if "$" in matches.group(2):
            registers[i][int(matches.group(2)[1:])] = 1
    matches = pattern.match(i)
    if matches:
        registers[i][int(matches.group(2)[1:])] = 1
        registers[i][int(matches.group(1)[1:])] = 2
        if "$" in matches.group(3):
            registers[i][int(matches.group(3)[1:])] = 1
    matches = branchPattern.match(i)
    if matches:
        registers[i][int(matches.group(1)[1:])] = 1
        registers[i][int(matches.group(2)[1:])] = 1


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


# print(registers[instructions[2]])
# print(registers[instructions[3]])
print(hasHazard("lw $r1, numOne", "lw $r2, 0($r1)"))
