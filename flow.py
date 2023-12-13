import pygame, sys, classes
from pygame.locals import *

def display_boxes(boxes):
    for p in boxes:
            p.display()

def get_line_positions(start: tuple, end: tuple):
    half_width = 50
    li = [start]
    if start[1] + 20 > end[1]:
        if start[0] < end[0] + 120 and start[0]  + 120 > end[0]:
            li.append((start[0], start[1]+10))
            if start[0] > end[0]:
                li.append(((start[0] - (half_width+10)), start[1]+10))
                li.append(((start[0] - (half_width+10)), (start[1]+end[1])/2))
                li.append(((end[0] + (half_width+10)), (start[1]+end[1])/2))
                li.append(((end[0] + (half_width+10)), end[1]-10))
            else:
                li.append(((start[0] + (half_width+10)), start[1]+10))
                li.append(((start[0] + (half_width+10)), (start[1]+end[1])/2))
                li.append(((end[0] - (half_width+10)), (start[1]+end[1])/2))
                li.append(((end[0] - (half_width+10)), end[1]-10))
            li.append((end[0], end[1]-10))
        else:
            li.append((start[0], start[1]+10))
            li.append(((start[0]+end[0])/2, start[1]+10))
            li.append(((start[0]+end[0])/2, end[1]-10))
            li.append((end[0], end[1]-10))
    else:
        li.append((start[0], (start[1]+end[1])/2))
        li.append((end[0], (start[1]+end[1])/2))
    li.append(end)
    return li

def draw_line(boxes: list, indexs: tuple, boxes_index: list, width: int = 10):
    win = window
    index1 = boxes_index.index(indexs[0])
    start = (boxes[index1].x+(boxes[index1].w/2), boxes[index1].y + boxes[index1].h)
    if indexs[1] != -1:
        index2 = boxes_index.index(indexs[1])
        end = (boxes[index2].x + (boxes[index2].w/2), boxes[index2].y)
    else:
        end = pygame.mouse.get_pos()
    
    points = get_line_positions(start, end)
    for i in points[1:-1]:
        pygame.draw.circle(win, (255, 255, 255), (i[0]+1, i[1]+1), (width/2))
    pygame.draw.lines(win, (255, 255, 255), False, points, width)

pygame.init() #initailise pygame
pygame.display.set_caption("Flowchart") #set title
clock = pygame.time.Clock() # setup for framerate for consitiant animations
framerate = 120
width, height = 1920, 1009 #set height and width
window = pygame.display.set_mode((width, height), RESIZABLE) #show window
boxes = [] #set up the list to hold the box classes in
boxes_index = [] #set up list that keeps track of which box is which (so connections can be made between boxes while boxes are being moved around in lists)
boxes_connections = []
justline = False #justline is if a line was just connected
data = {'line to mouse': False, 'boxes with lines in': [], 'boxes with lines out': [], 'number of boxes': 1}

boxes.append(classes.draggable_box(10, 10, 100, 100, window, (25, 100, 100)))
boxes_index.append(0)


while True:
    w, h= pygame.display.get_surface().get_size() # get size of screen
    mx, my = pygame.mouse.get_pos() #get mouse position
    mpressed, _, rpressed = pygame.mouse.get_pressed() #get mouse pressing state
    pygame.draw.rect(window, (31, 31, 31), pygame.Rect(0, 0, w, h)) #fill screen with blank
    for event in pygame.event.get(): #checking events
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if not rpressed: #if the right click is not pressed:
        justline = False #there must not be a line
    selected = False #selected is true for when a box i being dragged
    for i in boxes_connections:
        draw_line(boxes, i, boxes_index)
    
    for i, box in enumerate(boxes): #this checks whether a box is selected
        if box.selected: #the box.selected is a variable telling whether the box is selected
            boxes.append(boxes.pop(i)) #this moves the selcted box to the back so it is displayed at the front (boxes at the front are displayed first, so boxes at the back are displayed last)
            boxes_index.append(boxes_index.pop(i))
            print(box.selected)
            if i == 0:
                data['number of boxes'] +=1
                boxes.insert(0, classes.draggable_box(10, 10, 100, 100, window, (25, 100, 100)))
                boxes_index.insert(0, data['number of boxes'])
            selected = True #the box is set to being dragged
            break #no need to check for more boxes being selected because only one box can be selected at once
    
    if selected and not data['line to mouse']: #if a box is selected:
        boxes[-1].update() #only the last element needs to be updated, see above
        for i in boxes: #all the elements need to be returned to their original colour except the last, as it is selected (if a box is selected, no boxes should be shaded)
            i.return_to_normal_colour() #return to unshaded
    else:
        hov = False #is one of the boxes being hovered on (only one box is allowed to be hovered on at once)
        for p, i in enumerate(reversed(boxes)): #reversed because the boxes displayed at the front are actually at the back
            if i.hover() and not hov: #if the box is being hovered on and this is the first box to be hovered on
                hov = True
                i.set_selected() #only the box being hovered on needs to be updated
                i.change_colour()
            else:
                i.return_to_normal_colour()
            if i.rclick(): #if the box is being leftpressed on
                if not data['line to mouse'] and not justline and not boxes_index[(len(boxes)-p)-1] in data['boxes with lines out']: #if there is not a line to the mouse, and a line was not just created and, this box is does not have a line coming out of it already
                    boxes_connections.append((boxes_index[(len(boxes)-p)-1], -1)) #append a tuple containing the 'true' index of this box and -1 (-1 denotes a line to mouse)
                    data['line to mouse'] = True #so another line to mouse cannot be made
                    data['boxes with lines out'].append(boxes_index[(len(boxes)-p)-1]) #so another line cannot be made out of this box
                    justline = True
                elif boxes_connections[-1][0] != boxes_index[(len(boxes)-p)-1] and not boxes_index[(len(boxes)-p)-1] in data['boxes with lines in']: #if the box is not the box that the line is coming out of and this box does not have a line in already
                    boxes_connections[-1] = (boxes_connections[-1][0], boxes_index[(len(boxes)-p)-1]) #the second element of the tuple is set to the current box
                    data['line to mouse'] = False #as the line has been connected to this box it is no longer connected to the mouse
                    data['boxes with lines in'].append(boxes_index[(len(boxes)-p)-1]) #this box now has a line into it
                    justline = True #so the box does not emediatly have a line from it
        if rpressed and data['line to mouse'] and not justline:
            data['line to mouse'] = False
            data['boxes with lines out'] = data['boxes with lines out'][:-1]
            boxes_connections = boxes_connections[:-1]
    display_boxes(boxes)
    pygame.display.flip() #update
    clock.tick(framerate) 