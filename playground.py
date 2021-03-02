import re

variable = ['hello_world: .asciiz "hello world\n"', "num: .word 7", "num2: .word 7"]
string_pattern = re.compile(r'(\w+:)\s*(\.[a-z]+)\s*(.+\s*.*)')

for i in variable:
    match = string_pattern.match(i)
    if match:
        print(match.group(1).encode("unicode-escape"))