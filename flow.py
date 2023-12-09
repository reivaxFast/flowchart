import pygame, sys, classes
from pygame.locals import *

def display_boxes(boxes):
    for p in boxes:
            p.display()
            
def draw_line(boxes: list, indexs: tuple, boxes_index: list):
    index1 = boxes_index.index(indexs[0])
    if indexs[1] != -1:
        index2 = boxes_index.index(indexs[1])
        pygame.draw.line(window, (255, 255, 255), (boxes[index1].x+(boxes[index1].w/2), boxes[index1].y + boxes[index1].h), (boxes[index2].x + (boxes[index2].w/2), boxes[index2].y), 10)
    else:
        pygame.draw.line(window, (255, 255, 255), (boxes[index1].x+(boxes[index1].w/2), boxes[index1].y + boxes[index1].h), pygame.mouse.get_pos(), 10)

pygame.init() #initailise pygame
pygame.display.set_caption("Flowchart") #set title
clock = pygame.time.Clock() # setup for framerate for consitiant animations
framerate = 60
width, height = 1920, 1009 #set height and width
window = pygame.display.set_mode((width, height), RESIZABLE) #show window
boxes = [] #set up the list to hold the box classes in
boxes_index = [] #set up list that keeps track of which box is which (so connections can be made between boxes while boxes are being moved around in lists)
boxes_connections = []
justline = False
data = {'line to mouse': False, 'boxes with lines in': [], 'boxes with lines out': []}
for i in range(10):
    boxes.append(classes.draggable_box(200*i, 10, 100, 100, window, (25 * i, 100, 100)))
    boxes_index.append(i)


while True:
    w, h= pygame.display.get_surface().get_size() # get size of screen
    mx, my = pygame.mouse.get_pos() #get mouse position
    mpressed, _, rpressed = pygame.mouse.get_pressed() #get mouse pressing state
    pygame.draw.rect(window, (31, 31, 31), pygame.Rect(0, 0, w, h)) #fill screen with blank
    for event in pygame.event.get(): #chacking events
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if not rpressed:
        justline = False
    selected = False #selected is true for when a box i being dragged
    for i in boxes_connections:
        draw_line(boxes, i, boxes_index)
    
    for i, box in enumerate(boxes): #this checks whether a box is selected
        if box.selected: #the box.selected is a variable telling whether the box is selected
            boxes.append(boxes.pop(i)) #this moves the selcted box to the back so it is displayed at the front (boxes at the front are displayed first, so boxes at the back are displayed last)
            boxes_index.append(boxes_index.pop(i))
            selected = True #the box is set to being dragged
            break #no need to check for more boxes being selected because only one box can be selected at once
    
    if selected: #if a box is selected:
        boxes[-1].update() #only the last element needs to be updated, see above
        for i in boxes[:-1]: #all the elements need to be returned to their original colour except the last, as it is selected (if a box is selected, no boxes should be shaded)
            i.return_to_normal_colour() #return to unshaded
        display_boxes(boxes)
    else:
        hov = False
        for p, i in enumerate(reversed(boxes)):
            if i.hover() and not hov:
                i.update()
                hov = True
                i.update() #only the box being hovered on needs to be updated
            else: #all other boxes need to be returned to normal colour
                i.return_to_normal_colour()
            if i.rclick():
                if not data['line to mouse'] and not justline and not boxes_index[(len(boxes)-p)-1] in data['boxes with lines out']:
                    boxes_connections.append((boxes_index[(len(boxes)-p)-1], -1))
                    data['line to mouse'] = True
                    data['boxes with lines out'].append(boxes_index[(len(boxes)-p)-1])
                elif boxes_connections[-1][0] != boxes_index[(len(boxes)-p)-1] and not boxes_index[(len(boxes)-p)-1] in data['boxes with lines in']:
                    boxes_connections[-1] = (boxes_connections[-1][0], boxes_index[(len(boxes)-p)-1])
                    data['line to mouse'] = False
                    data['boxes with lines in'].append(boxes_index[(len(boxes)-p)-1])
                    justline = True
        display_boxes(boxes)
    pygame.display.flip() #update
    clock.tick(framerate) 