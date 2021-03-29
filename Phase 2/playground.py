import re

pattern = re.compile(r"[lsw]{2}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\d*\(\$([a-z][0-9])\)")
string = "lw $r1, 0($r2)"
matches = pattern.match(string)
print(matches.group(1))