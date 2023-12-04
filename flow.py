import pygame, sys, classes
from pygame.locals import *

def display_boxes(boxes):
    for p in boxes:
            p.display()

pygame.init() #initailise pygame
pygame.display.set_caption("Flowchart") #set title
clock = pygame.time.Clock() # setuo for framerate for consitiant animations
framerate = 60
width, height = 1920, 1009 #set height and width
window = pygame.display.set_mode((width, height), RESIZABLE) #show window
boxes = [] #set up the list to hold
for i in range(10):
    boxes.append(classes.draggable_box(200*i, 10, 100, 100, window, (25 * i, 100, 100)))


while True:
    w, h= pygame.display.get_surface().get_size() # get size of screen
    mx, my = pygame.mouse.get_pos() #get mouse position
    mpressed, _, _ = pygame.mouse.get_pressed() #get mouse pressing state
    pygame.draw.rect(window, (31, 31, 31), pygame.Rect(0, 0, w, h)) #fill screen with blank
    for event in pygame.event.get(): #chacking events
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    selected = False #selected is true for when a box i being dragged
    
    for i, box in enumerate(boxes): #this checks whether a box is selected
        if box.selected: #the box.selected is a variable telling whether the box is selected
            boxes.append(boxes.pop(i)) #this moves the selcted box to the back so it is displayed at the front (boxes at the front are displayed first, so boxes at the back are displayed last)
            selected = True #the box is set to being dragged
            break #no need to check for more boxes being selected because only one box can be selected at once
    if selected: #if a box is selected:
        boxes[-1].update() #only the last element needs to be updated, see above
        for i in boxes[:-1]: #all the elements need to be returned to their original colour except the last, as it is selected (if a box is selected, no boxes should be shaded)
            i.return_to_normal_colour() #return to unshaded
        display_boxes(boxes)
    else: #if no box is selected
        hov = False #is a box veing hovered on?
        for i in reversed(boxes): #reversed because boxes at the back of the list appear to be at the front and so need to be updated first
            if i.hover() and not hov: #if the box i is being hovered on and no other boxes can be hovered on (only one box can be hovered on at once)
                hov = True
                i.update() #only the box being hovered on needs to be updated
            else: #all other boxes need to be returned to normal colour
                i.return_to_normal_colour()
        display_boxes(boxes)
    
    pygame.display.flip() #update
    clock.tick(framerate) 