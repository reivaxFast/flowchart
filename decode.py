'''
SYNTAX:
variables must start with a capital


commands:
OUTPUT 
INPUT


'''
#types of boxes:
#start: at the start of the algorithm: 'START'
#end: end of flowchart: 'END'
#proscess: e.g. declaring/changing variables: 'PRO'
#input/output: 'IO'
#descision (if statement): 'IF'
def get_code(boxes, boxes_indexes):
    code = []
    types = []
    new_boxes = [i for i in range(len(boxes))]
    for i, j in enumerate(boxes_indexes):
        new_boxes[j] = boxes[i]
    for i in new_boxes:
        code.append(i.text)
        types.append(i.type)
    return code, types

def get_type(strin):
    if strin[0] == '\'':
        return 'str'
    elif strin[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        return 'int'
    elif strin[0] in ['+', '-', '*', '/']:
        return 'opp'
    else:
        return 'var'

def decode(code: list, lines, types):
    where = 0
    variables = {}
    for j, i in enumerate(types):
        if i == 'START':
            start = j
            where = start
            break
    end = False
    output = []
    result = False
    while not end:
        for j, i in enumerate(lines):
            if i[0] == where:
                if not result:
                    where = i[1]
                    box_type = types[where]
                    current = code[where].split('\n')
                    if box_type == 'END':
                        end = True
                        break
                    elif box_type == 'PRO':
                        for i in current:  
                            split = i.split(' ')
                            ty = get_type(split[2])
                            if ty == 'str':
                                variables[split[0]] = split[2][1:-1]
                            elif ty == 'int':
                                variables[split[0]] = float(split[2])
                            elif ty == 'var':
                                ev = ''
                                for i in split[2:]:
                                    if get_type(i) == 'var':
                                        ev = ev + str(variables[i])
                                    else:
                                        ev = ev+str(i)
                                variables[split[0]] = eval(ev)
                    elif box_type == 'IO':
                        for i in current:  
                            split = i.split(' ')
                            match split[0]:
                                case 'OUTPUT':
                                    ty = get_type(split[2])
                                    match ty:
                                        case 'str':
                                            output.append(split[2][1:-1])
                                        case 'int':
                                            output.append(split[2])
                                        case 'var':
                                            output.append(variables[split[2]])
                                case 'INPUT':
                                    variables[split[2]] = input()
                                case _:
                                    raise Exception('invalid input/output')
                    elif box_type == 'IF':
                        split = current[0].split(' ')
                        ev = ''
                        for i in split[3:]:
                            if get_type(i) == 'var':
                                ev = ev + str(variables[i])
                            else:
                                ev = ev+str(i)
                        result = eval(f'{variables[split[1]]} {split[2]} {ev}')
                    break
                else:
                    result = False
            elif j == len(lines)-1:
                output = ['error!']
    return output
#print(decode(['START', 'INPUT >> Hello','Hello = Hello / 10', 'if Hello == Hello', 'OUTPUT << Hello','END'], [(0, 1), (1, 2), (2, 3), (3, 5), (3, 4), (4, 5)], ['START', 'IO', 'PRO', 'IF', 'IO', 'END']))