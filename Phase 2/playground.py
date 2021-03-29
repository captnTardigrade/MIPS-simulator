import re

pattern = re.compile(
    r"\w{2,3}[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])[ \t]*,[ \t]*\$([a-z][0-9])")
string = "sub $r4, $r1, $r5"
matches = pattern.match(string)
print(matches.group(1))
