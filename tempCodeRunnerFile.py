import re
string_pattern = re.compile(r'(\w+:)\s*(\.[a-z]+)\s*(.+\s)')

f = open("hello_world.asm", "r")
matches = string_pattern.finditer(f.read())

for match in matches:
    if match:
        print(match.group(2).strip())