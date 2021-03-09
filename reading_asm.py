import re

# primitive data types
primitives = (".asciiz", ".word", ".byte")

# matches variables using the following pattern
var_pattern = re.compile(r'(\w+:)\s*(\.[a-z]+)\s*(.+\s)')

# matches labels with along with instructions
label_pattern = re.compile(
    r"(\w+:(?!\s*\.))(\s*\w{2,3}\s*(\$[a-z0-9]{2}\s*,?\s*)*([^\n]*))*")

path = r"./instructionTest.asm"


def getData(path):
    '''
        extracts variables and stores them in
        a dictionary with variable names as keys

        returns the dictionary
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


def getInstructions(path):
    '''
        stores the instructions present in a label
        in a dictionary of labels as keys and list of instructions
        as values

        returns the dictionary
    '''
    f = open(path, "r") # instructionTest.asm refers to the above asm code
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

    return instructions