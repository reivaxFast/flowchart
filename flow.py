import pygame, sys, classes
from pygame.locals import *

def display_boxes(boxes):
    for p in boxes:
            p.display()
            
def draw_line(boxes: list, indexs: tuple):
    if indexs[1] != -1:
        pygame.draw.line(window, (255, 255, 255), (boxes[indexs[0]].x, boxes[indexs[0]].y), (boxes[indexs[1]].x, boxes[indexs[1]].y), 10)
    else:
        pygame.draw.line(window, (255, 255, 255), (boxes[indexs[0]].x, boxes[indexs[0]].y), pygame.mouse.get_pos(), 10)

pygame.init() #initailise pygame
pygame.display.set_caption("Flowchart") #set title
clock = pygame.time.Clock() # setup for framerate for consitiant animations
framerate = 60
width, height = 1920, 1009 #set height and width
window = pygame.display.set_mode((width, height), RESIZABLE) #show window
boxes = [] #set up the list to hold the box classes in
boxes_index = [] #set up list that keeps track of which box is which (so connections can be made between boxes while boxes are being moved around in lists)
boxes_connections = []
for i in range(10):
    boxes.append(classes.draggable_box(200*i, 10, 100, 100, window, (25 * i, 100, 100)))
    boxes_index.append(i)


while True:
    w, h= pygame.display.get_surface().get_size() # get size of screen
    mx, my = pygame.mouse.get_pos() #get mouse position
    mpressed, _, _ = pygame.mouse.get_pressed() #get mouse pressing state
    pygame.draw.rect(window, (31, 31, 31), pygame.Rect(0, 0, w, h)) #fill screen with blank
    pygame.draw.line(window, (255, 255, 255), (10, 10), (300, 60), 5)
    for event in pygame.event.get(): #chacking events
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    selected = False #selected is true for when a box i being dragged
    
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
            else:
                i.return_to_normal_colour()
            if i.rclick():
                boxes_connections.append((boxes_index[p], -1))
        display_boxes(boxes)
    for i in boxes_connections:
        draw_line(boxes, i)
    pygame.display.flip() #update
    clock.tick(framerate)