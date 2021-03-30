import re

# instructions = ["lw $r1, 0($r2)", "sub $r4, $r1, $r5",
#                 "and $r6, $r1, $r7", "or $r8, $r1, $r9"]
instructions = ["sub $r4, $r1, $r5", "and $r6, $r1, $r7"]

registers = [[0 for _ in range(10)] for _ in instructions]

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


def hasHazard(i1, i2):
    for i in range(len(registers[0])):
        if (registers[i1][i] == 1 and registers[i2][i] == 2) or (registers[i1][i] == 2 and registers[i2][i] == 2):
            return True
    return False


print(hasHazard(1, 0))
