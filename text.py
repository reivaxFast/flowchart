import pygame
import math

def render_text_in_box(textvalue: str, surface: pygame.Surface, box_position: tuple, box_size: tuple, colour = (0,0,0), text_type = 'freesansbold.ttf'):
    lines = textvalue.split('\n')
    curr_size =(box_size[1]//len(lines))+1
    largest_x = box_size[0]+1
    while largest_x > box_size[0]:
        font = pygame.font.Font(text_type, curr_size)
        largest_x = 0
        for i in lines:
            curr_x = font.render(i, True, (255, 255, 255)).get_rect().width
            if curr_x > largest_x:
                largest_x = curr_x
        curr_size -= 1
    font = pygame.font.Font(text_type, curr_size)
    texts = [font.render(x, True, colour) for x in lines]
    for i, text in enumerate(texts):
        surface.blit(text, (box_position[0], box_position[1]+(curr_size*i)))