import pygame

def gradient(colour_1: tuple, colour_2: tuple, gadient: float):
    ret = (0,0,0)
    for i in range(3):
        ret[i] = (colour_1 * (1-gadient)) + (colour_1 * gadient)
    return ret

class draggable_box:
    def __init__(self, x: int, y: int, w: int, h: int, normal_colour: tuple = (255, 255, 255), shaded_colour: tuple = (200, 200, 200)) -> None:
        self.x = x #x position
        self.y = y #y position
        self.w = w #width
        self.h = h #height
        self.colour = normal_colour #colour
        self.normal_colour = normal_colour #default colour
        self.shaded_colour = shaded_colour #shaded colour
        self.gradient = 0 #how far between shaded and default is the colour (0 is unshaded, 1 is shaded)
        self.selected = True #is the box being moved?
        self.mpessedlast = False #was the mouse being pressed last frame (so the box can only be selected if clicked on)
        
    def update(self, screen):
        mx, my = pygame.mouse.get_pos() # getting mouse position
        mpressed, _, _ = pygame.mouse.get_pressed() #getting mouse state
        if self.hover() and not self.selected:
            c, _, _ = self.colour #getting the colour
            p = max(c-10, self.shaded_colour[0]) #for a smooth darkening
            self.colour = (p, p, p)
            if mpressed and not self.mpessedlast:
                self.selected = True
                self.offsetx = self.x - mx
                self.offsety = self.y - my
        else:
            c, _, _ = self.colour
            p = min(c+10, self.normal_colour[0])
            self.colour = (p, p, p)
        
        if self.selected and mpressed:
            self.x = mx + self.offsetx
            self.y = my + self.offsety
        else:
            self.selected = False
        pygame.draw.rect(screen, self.colour, pygame.Rect((self.x, self.y), (self.w,self.h)))
        self.mpessedlast = mpressed
    
    def hover(self):
        mx, my = pygame.mouse.get_pos()
        if self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h:
            return True
        else:
            return False