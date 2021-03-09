## This is an experimental file, to test out different things

# import re
# label_pattern = re.compile(r'([a-z]{2,3}\s*(\$[a-z0-9]{2}),?\s*((\$[a-z0-9]{2},?\s){2}|.*))')
# label_pattern = re.compile(
#     r'''(\w+:)(\s*([^.]{2,3})\s*(\$[a-z0-9]{2},?\s*)(((\$[a-z0-9]{2},?\s*){2,3}))+)+''')

# label_pattern = re.compile(
#     r"(\w+:)(\s*\w{2,3}\s*(\$[a-z0-9]{2}\s*,?\s*){1,3}\s*((\d+\(\$[a-z][0-9]\)))*\n?)+")


import re

label_pattern = re.compile(
    r"(\w+:(?!\s*\.))(\s*\w{2,3}\s*(\$[a-z0-9]{2}\s*,?\s*)*([^\n]*))*")

test_pattern = re.compile(
    r"\s*\w{2}\s*\$[a-z][0-9]\s*,\s*(\d+\(\$[a-z][0-9]\))*\w+\s*"
) # this pattern matches the instruction lw $s2, numOne

f = open("instructionTest.asm", "r") # instructionTest.asm refers to the above asm code
matches = label_pattern.finditer(f.read())
l = []
for match in matches:
    if match:
        l.extend([i.strip() for i in match.group().split("\n") if i.strip()])
instructions = {}
for i in range(len(l)):
    if ":" in l[i]:
        instructions[l[i][:-1]] = []
        j = i + 1
        while j < len(l) and (not ":" in l[j]):
            instructions[l[i][:-1]].append(l[j])
            j += 1
print(instructions)