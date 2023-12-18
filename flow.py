import pygame, sys, classes, lines
from pygame.locals import *

def display_boxes(boxes):
    for p in boxes:
            p.display()

#general setup
pygame.init() #initailise pygame
pygame.display.set_caption("Flowchart") #set title
clock = pygame.time.Clock() # setup for framerate for consitiant animations
framerate = 120
width, height = 1920, 1009 #set height and width
window = pygame.display.set_mode((width, height), RESIZABLE) #show window
#colours
boxes_colour = (25, 100, 100)
bg_colour = (31, 31, 31)

boxes = [] #set up the list to hold the box classes in
boxes_index = [] #set up list that keeps track of which box is which (so connections can be made between boxes while boxes are being moved around in lists)
boxes_connections = []
justline = False #justline is if a line was just connected
data = {'line to mouse': False, 'boxes with lines in': [], 'boxes with lines out': []}

boxes.append(classes.draggable_box(10, 10, 200, 75, window, boxes_colour, box_type='pro'))
boxes.append(classes.draggable_box(10, 95, 200, 75, window, boxes_colour, box_type='if'))
boxes.append(classes.draggable_box(10, 180, 200, 75, window, boxes_colour, box_type='io'))
boxes.append(classes.draggable_box((width/2)-100, 10, 200, 75, window, boxes_colour, box_type='start'))
boxes.append(classes.draggable_box((width/2)-100, height - 95, 200, 75, window, boxes_colour, box_type='end'))
for i in range(len(boxes)):
    boxes_index.append(i)


while True:
    w, h= pygame.display.get_surface().get_size() # get size of screen
    mx, my = pygame.mouse.get_pos() #get mouse position
    mpressed, _, rpressed = pygame.mouse.get_pressed() #get mouse pressing state
    window.fill(bg_colour) #fill screen with blank
    for event in pygame.event.get(): #checking events
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if not rpressed: #if the right click is not pressed:
        justline = False #there must not be a line
    selected = False #selected is true for when a box i being dragged
    for i in boxes_connections:
        lines.draw_line(boxes, i, boxes_index, window)
    
    for i, box in enumerate(boxes): #this checks whether a box is selected
        if box.selected: #the box.selected is a variable telling whether the box is selected
            boxes.append(boxes.pop(i)) #this moves the selcted box to the back so it is displayed at the front (boxes at the front are displayed first, so boxes at the back are displayed last)
            boxes_index.append(boxes_index.pop(i))
            if i in [0, 1, 2]:
                boxes.insert(i, classes.draggable_box(box.x , box.y, box.w, box.h, window, boxes_colour, box_type= box.type))
                boxes_index.insert(i, len(boxes) + 1)
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
                if not data['line to mouse'] and not justline and not boxes_index[(len(boxes)-p)-1] in data['boxes with lines out'] and not i.type == 'end': #if there is not a line to the mouse, and a line was not just created and, this box is does not have a line coming out of it already
                    boxes_connections.append((boxes_index[(len(boxes)-p)-1], -1)) #append a tuple containing the 'true' index of this box and -1 (-1 denotes a line to mouse)
                    data['line to mouse'] = True #so another line to mouse cannot be made
                    data['boxes with lines out'].append(boxes_index[(len(boxes)-p)-1]) #so another line cannot be made out of this box
                    justline = True
                elif boxes_connections[-1][0] != boxes_index[(len(boxes)-p)-1] and not boxes_index[(len(boxes)-p)-1] in data['boxes with lines in'] and not i.type == 'start': #if the box is not the box that the line is coming out of and this box does not have a line in already
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