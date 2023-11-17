import pygame

class draggable_box:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    def update(self, screen):
        self.x, self.y = pygame.mouse.get_pos()
        pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect((self.x, self.y), (100,100)))