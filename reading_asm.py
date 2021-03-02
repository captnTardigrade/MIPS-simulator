import re

## primitive data types
primitives = (".asciiz", ".word", ".byte")

## variable pattern
var_pattern = re.compile(r'(\w+:)\s*(\.[a-z]+)\s*(.+\s*.*)')

def read_file(path):
    '''
    read an asm file at a specified path and returns 
    a list of each non-empty line

    '''
    
    f = open(r'{}'.format(path), "r")
    lines = [i.strip() for i in f.readlines() if i.strip() != '']
    return lines

def fillData(lines):
    data = {}
    for i in lines:
        match = var_pattern.match(i)
        if match:
            var_name = match.group(1)[:-1]
            var_type = match.group(2)
            var_value = match.group(3)
            if var_type == primitives[1]:
                var_value = int(var_value)
            data[var_name] = var_value
    
    return data

data = fillData(read_file("./hello_world.asm"))
print(data)