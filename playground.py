## This is an experimental file, to test out different things

import re
# label_pattern = re.compile(r'([a-z]{2,3}\s*(\$[a-z0-9]{2}),?\s*((\$[a-z0-9]{2},?\s){2}|.*))')
label_pattern = re.compile(
    r"(\w+:)(\s*([^.][a-z]{2,3})\s*(\$[a-z0-9]{2},?\s*)(((\$[a-z0-9]{2},?\s*){2,3})|.*)+)+")

f = open("add.asm", "r")
matches = label_pattern.finditer(f.read())

for match in matches:
    if match:
        l = [i.strip() for i in match.group().split("\n")[1:]]
        print(l)
