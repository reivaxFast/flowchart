import pygame

class draggable_box:
    def __init__(self, x: int, y: int, w: int, h: int, window, normal_colour: tuple = (255, 255, 255), shaded_colour: tuple = (200, 200, 200), gradient_speed: float = 0.1) -> None:
        self.x = x #x position
        self.y = y #y position
        self.w = w #width
        self.h = h #height
        self.window = window #window
        self.colour = normal_colour #colour
        self.normal_colour = normal_colour #default colour
        self.shaded_colour = shaded_colour #shaded colour
        self.gradient = 0 #how far between shaded and default is the colour (0 is unshaded, 1 is shaded)
        self.gradient_speed = gradient_speed #how fast to change the gradient
        self.selected = True #is the box being moved?
        self.mpressedlast = False #was the mouse being pressed last frame (so the box can only be selected if clicked on)
        self.rpressedlast = False
        
    def update(self):
        mx, my = pygame.mouse.get_pos() # getting mouse position
        mpressed, rpressed, _ = pygame.mouse.get_pressed() #getting mouse state
        if self.hover() and not self.selected:
            self.colour = self.return_gradient(1)
            if mpressed and not self.mpressedlast:
                self.selected = True
                self.offsetx = self.x - mx
                self.offsety = self.y - my
        else:
            self.colour = self.return_gradient(-1)
        
        if self.selected and mpressed:
            self.x = mx + self.offsetx
            self.y = my + self.offsety
        else:
            self.selected = False
        self.mpressedlast = mpressed
        self.rpressedlast = rpressed
    
    def display(self):
        pygame.draw.rect(self.window, self.colour, pygame.Rect((self.x, self.y), (self.w,self.h)))
    
    def return_to_normal_colour(self):
        self.colour = self.return_gradient(-1)
    
    def hover(self):
        mx, my = pygame.mouse.get_pos()
        if self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h:
            return True
        else:
            return False
    
    def return_gradient(self, change: int): #in change, -1 decreases, 0 does not change, 1 increases the gradient variable
        ret = [0,0,0] #list to be returned
        for i in range(3): #
            ret[i] = (self.normal_colour[i] * (1-self.gradient)) + (self.shaded_colour[i] * self.gradient)
        self.gradient += change * self.gradient_speed
        self.gradient = max(0, min(1, self.gradient))
        return tuple(ret)
    
    def rclick(self):
        mpressed, rpressed, _ = pygame.mouse.get_pressed()
        if rpressed and not self.rpressedlast and self.hover():
            return True
        else:
            return False