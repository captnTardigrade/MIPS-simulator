import re

## primitive data types
primitives = (".asciiz", ".word", ".byte")

## variable pattern
var_pattern = re.compile(r'(\w+:)\s*(\.[a-z]+)\s*(.+\s)')

def fillData(path):
    '''
        extracts variables and fills
        data
    '''
    f = open(r'{}'.format(path), "r")
    data = {}
    matches = var_pattern.finditer(f.read())
    for match in matches:
        if match:
            var_name = match.group(1)[:-1]
            var_type = match.group(2)
            var_value = match.group(3).strip()
            if var_type == primitives[1]:
                try:
                    var_value = int(var_value)
                except ValueError:
                    var_value = [int(i.strip()) for i in var_value.split(",")]
            data[var_name] = var_value
    
    return data

data = fillData("./hello_world.asm")
print(data)