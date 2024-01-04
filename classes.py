import pygame, text, time, keyboard
class draggable_box:
    def __init__(self, x: int, y: int, w: int, h: int, window: pygame.Surface, normal_colour: pygame.Color = (255, 255, 255), shaded_colour: tuple = (200, 200, 200), gradient_speed: float = 0.1, box_type: str = 'pro', max_text_size: int = 15) -> None:
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
        self.drag_type = 0 #e.g. if it is being moved, of resized (0 is moved, 1 is horizobtal, 2 is vertical, 3 is both vertical and horizontal)
        self.start_selected_time = 0 #this is for weather it is clicked or not
        self.max_text_size = max_text_size
        self.writing_position = (0,0) #where in the lines the cursor is
        self.resize_offsetx = 0
        self.resize_offsety = 0
        match self.type:
            case 'start': 
                self.text = 'START'
                self.centered = True
                self.numbered_lines = False
            case 'end': 
                self.text = 'END'
                self.centered = True
                self.numbered_lines = False
            case _: 
                self.text = ''
                self.centered = False
                self.numbered_lines = True
        self.keys_pressed_last = []
        self.key_pressed_times = []
        self.alphabet =   'abcdefghijklmnopqrstuvwxyz1234567890\n    -='
        self.shift_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!"£$%^&*()_+'
        self.update_display_lines()
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
            self.start_selected_time = time.time()
            self.selected = True
            self.offsetx = self.x - mx
            self.offsety = self.y - my
    
    def update(self):
        mx, my = pygame.mouse.get_pos() # getting mouse position
        mpressed, _, rpressed = pygame.mouse.get_pressed() #getting mouse state
        click_speed = 0.15
        writing = False
        if self.drag_type == 0:
            if self.hover() and not self.selected and mpressed and not self.mpressedlast:
                self.start_selected_time = time.time()
                self.selected = True
                self.offsetx = self.x - mx
                self.offsety = self.y - my
            
            if self.selected and mpressed:
                if time.time()-self.start_selected_time > click_speed and not writing:
                    self.x = mx + self.offsetx
                    self.y = my + self.offsety
            else:
                self.selected = False
                if time.time()-self.start_selected_time < click_speed and  not self.type in ['start', 'end']:
                    self.drag_type = 4
        elif mpressed:
            match self.drag_type:
                case 1: self.w = max((mx - self.x)+self.resize_offsetx, 100)
                case 2: self.h = max((my - self.y)+self.resize_offsety, 35)
                case 3: self.w, self.h = (max((mx - self.x)+self.resize_offsetx, 100), max((my - self.y)+self.resize_offsety, 35))
            self.update_display_lines()
        self.mpressedlast = mpressed
        self.rpressedlast = rpressed
    
    def display(self):
        match self.type:
            case 'pro': 
                pygame.draw.rect(self.window, self.colour, pygame.Rect((self.x, self.y), (self.w,self.h)))
                text.render_text_in_box(self.display_text, self.window, (self.x, self.y), (self.w, self.h), self.text_size, (0,0,0), self.centered)
            case 'start': 
                pygame.draw.rect(self.window, self.colour, pygame.Rect((self.x, self.y), (self.w,self.h)), border_radius=10)
                text.render_text_in_box(self.display_text, self.window, (self.x, self.y), (self.w, self.h), self.text_size, (0,0,0), self.centered)
            case 'end': 
                pygame.draw.rect(self.window, self.colour, pygame.Rect((self.x, self.y), (self.w,self.h)), border_radius=10)
                text.render_text_in_box(self.display_text, self.window, (self.x, self.y), (self.w, self.h), self.text_size, (0,0,0), self.centered)
            case 'io': 
                pygame.draw.polygon(self.window, self.colour, [(self.x + (self.h / 2), self.y), (self.x + self.w, self.y), ((self.x + self.w)-(self.h / 2), self.y + self.h), (self.x, self.y + self.h)])
            case 'if': 
                pygame.draw.polygon(self.window, self.colour, [(self.x, self.y + (self.h / 2)), (self.x + (self.w / 2), self.y), (self.x + self.w, self.y + (self.h / 2)), (self.x + (self.w / 2), self.y + self.h)])
        
    
    def return_to_normal_colour(self):
        self.colour = self.return_gradient(-1)
        
    def change_colour(self):
        if self.hover():
            self.colour = self.return_gradient(1)
        else:
            self.colour = self.return_gradient(-1)
    
    def hover(self, one = (1000000000000000, 1000000000000000)):
        mx, my = pygame.mouse.get_pos()
        if one[0] != 1000000000000000:
            mx, my = one
        if self.type in ['pro', 'start', 'end']:
            return self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h
        elif self.type == 'io':
            return (-0.5 * my)+self.x+(0.5*(self.h+self.y)) <= mx <= (-0.5 * my)+self.x+self.w + (0.5*self.y) and self.y <= my <= self.y + self.h
        elif self.type == 'if':
            return (my*-(self.w/self.h))+self.x+(self.w/2)+((self.y*self.w)/self.h) <= mx <= (my*-(self.w/self.h))+self.x+((3*self.w)/2)+((self.y*self.w)/self.h) and (my*(self.w/self.h))+self.x-(self.w/2)-((self.y*self.w)/self.h) <= mx <= (my*(self.w/self.h))+self.x+(self.w/2)-((self.y*self.w)/self.h)
    
    def edge(self):
        mx, my = pygame.mouse.get_pos()
        mpressed, _, rpressed = pygame.mouse.get_pressed() #getting mouse state
        margin = 10
        drag_type = 0
        #0 is not hover, 1 is horizontal, 2 is vertical, 3 is diagonal, 4 is other diagonal
        if not mpressed:
            if self.type == 'if':
                if not self.hover((mx+margin, my+margin)):
                    drag_type = 3
            else:
                if not self.hover((mx + margin, my)):
                    drag_type += 1
                if not self.hover((self.x + (self.w/2), my + margin)):
                    drag_type += 2
            self.resize_offsetx = (self.x+self.w)-mx
            self.resize_offsety = (self.y+self.h)-my
        else:
            drag_type =  self.drag_type
        self.drag_type = drag_type
        return drag_type

    
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
    
    def write(self):
        if not self.is_text_full:
            keys = pygame.key.get_pressed()
            for i, event in enumerate(keys):
                if event and not keys[pygame.K_LCTRL] and not keys[pygame.K_RCTRL]:
                    if not i in self.keys_pressed_last or time.time() - self.key_pressed_times[self.keys_pressed_last.index(i)] > 0.5:
                        if i in range(4, len(self.alphabet)+4) and i != 42:
                            if not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]:
                                self.text = self.text + self.alphabet[i-4]
                            else:
                                self.text = self.text + self.shift_char[i-4]
                        elif i == 42:
                            self.text = self.text[:-1]
                        if not i in self.keys_pressed_last:
                            self.keys_pressed_last.append(i)
                            self.key_pressed_times.append(time.time())
                        self.update_display_lines()
                        if self.is_text_full:
                            if not self.text[-2:] == '\n':
                                self.text = self.text[:-1]
                            else:
                                self.text = self.text[:-2]
                                self.is_text_full = False
                            self.update_display_lines(True)
                elif i in self.keys_pressed_last:
                    self.key_pressed_times.pop(self.keys_pressed_last.index(i))
                    self.keys_pressed_last.pop(self.keys_pressed_last.index(i))
    
    def update_display_lines(self, no_update_is_text_full = False):
        if not no_update_is_text_full:
            self.display_text, self.text_size, self.is_text_full = text.return_lines_in_a_box(self.text, (self.w, self.h), 15, 10, self.numbered_lines)
        else:
            self.display_text, self.text_size, _ = text.return_lines_in_a_box(self.text, (self.w, self.h), 15, 10, self.numbered_lines)
        self.line_lengths = [len(x)-2 for x in self.display_text]