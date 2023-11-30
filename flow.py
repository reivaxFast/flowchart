import pygame, sys, classes
from pygame.locals import *

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
            boxes.append(boxes.pop(i)) #this moves the box
            selected = True
            break
    if selected:
        boxes[-1].update()

        for i in boxes:
            i.display()
    else:
        hov = False
        for i in reversed(boxes):
            if i.hover() and not hov:
                i.update()
                hov = True
            else:
                i.return_to_normal_colour()
        for i in boxes:
            i.display()
    
    pygame.display.flip() #update
    clock.tick(framerate)