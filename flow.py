import pygame, sys, classes
from pygame.locals import *
pygame.init()

width, height = 1920, 1009
window = pygame.display.set_mode((width, height), RESIZABLE)
pygame.display.set_caption("Flowchart")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    mx, my = pygame.mouse.get_pos()
    mpressed, _, _ = pygame.mouse.get_pressed()
    pygame.display.flip() #update