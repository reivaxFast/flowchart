import pygame

class draggable_box:
    def __init__(self, x: int, y: int, w: int, h: int, window: pygame.Surface, normal_colour: tuple = (255, 255, 255), shaded_colour: tuple = (200, 200, 200), gradient_speed: float = 0.1, box_type: str = 'pro') -> None:
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
        self.selected = False #is the box being moved?
        self.mpressedlast = False #was the mouse being pressed last frame (so the box can only be selected if clicked on)
        self.rpressedlast = False
        self.type = box_type.lower() #the type of box
        #types of boxes:
        #start: at the start of the algorithm: 'START'
        #end: end of flowchart: 'END'
        #proscess: e.g. declaring/changing variables: 'PRO'
        #input/output: 'IO'
        #descision (if statement): 'IF'
        
    def set_selected(self):
        mx, my = pygame.mouse.get_pos() # getting mouse position
        mpressed, _, rpressed = pygame.mouse.get_pressed() #getting mouse state
        if self.hover() and not self.selected and mpressed and not self.mpressedlast:
            self.selected = True
            self.offsetx = self.x - mx
            self.offsety = self.y - my
    
    def update(self):
        mx, my = pygame.mouse.get_pos() # getting mouse position
        mpressed, _, rpressed = pygame.mouse.get_pressed() #getting mouse state
        if self.hover() and not self.selected and mpressed and not self.mpressedlast:
            self.selected = True
            self.offsetx = self.x - mx
            self.offsety = self.y - my
        
        if self.selected and mpressed:
            self.x = mx + self.offsetx
            self.y = my + self.offsety
        else:
            self.selected = False
        self.mpressedlast = mpressed
        self.rpressedlast = rpressed
    
    def display(self):
        match self.type:
            case 'pro': pygame.draw.rect(self.window, self.colour, pygame.Rect((self.x, self.y), (self.w,self.h)))
            case 'start': pygame.draw.rect(self.window, self.colour, pygame.Rect((self.x, self.y), (self.w,self.h)), border_radius=10)
            case 'end': pygame.draw.rect(self.window, self.colour, pygame.Rect((self.x, self.y), (self.w,self.h)), border_radius=10)
            case 'io': pygame.draw.polygon(self.window, self.colour, [(self.x + (self.h / 2), self.y), (self.x + self.w, self.y), ((self.x + self.w)-(self.h / 2), self.y + self.h), (self.x, self.y + self.h)])
            case 'if': pygame.draw.polygon(self.window, self.colour, [(self.x, self.y + (self.h / 2)), (self.x + (self.w / 2), self.y), (self.x + self.w, self.y + (self.h / 2)), (self.x + (self.w / 2), self.y + self.h)])
    
    def return_to_normal_colour(self):
        self.colour = self.return_gradient(-1)
        
    def change_colour(self):
        if self.hover():
            self.colour = self.return_gradient(1)
        else:
            self.colour = self.return_gradient(-1)
    
    def hover(self):
        mx, my = pygame.mouse.get_pos()
        return self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h
    
    def return_gradient(self, change: int): #in change, -1 decreases, 0 does not change, 1 increases the gradient variable
        ret = [0,0,0] #list to be returned
        for i in range(3): #
            ret[i] = (self.normal_colour[i] * (1-self.gradient)) + (self.shaded_colour[i] * self.gradient)
        self.gradient += change * self.gradient_speed
        self.gradient = max(0, min(1, self.gradient))
        return tuple(ret)
    
    def rclick(self):
        _, _, rpressed = pygame.mouse.get_pressed()
        if rpressed and self.hover():
            return True
        else:
            return False