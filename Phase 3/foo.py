import re

temp = re.compile(r"lw[ \t]+(\$\w+)[ \t]*,[ \t]*(\d+)\((\$\w+)\)")
match = temp.match("lw $s0, 0($zero)")
print(match.group(3))