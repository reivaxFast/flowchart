import pygame, sys, classes
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Flowchart")
clock = pygame.time.Clock()
framerate = 60
width, height = 1920, 1009
window = pygame.display.set_mode((width, height), RESIZABLE)
box = classes.draggable_box(10, 10, 100, 100)

while True:
    w, h= pygame.display.get_surface().get_size()
    pygame.draw.rect(window, (31, 31, 31), pygame.Rect(0, 0, w, h))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    mx, my = pygame.mouse.get_pos()
    mpressed, _, _ = pygame.mouse.get_pressed()
    
    box.update(window)
    pygame.display.flip() #update
    clock.tick(framerate)