'''
SYNTAX:
variables must start with a capital


commands:
OUTPUT 
INPUT


'''

def get_code(boxes, boxes_indexes):
    code = []
    new_boxes = [i for i in range(len(boxes))]
    for i, j in enumerate(boxes_indexes):
        new_boxes[j] = boxes[i]
    for i in boxes:
        code.append(i.text)

def decode(code, lines):
    for j, i in enumerate(code):
        if i == 'start':
            start = j
            break
    
