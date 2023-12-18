import pygame

def render_text_in_box(textvalue: str, surface: pygame.Surface, box_position: tuple, box_size: tuple, colour = (0,0,0), text_type = 'freesansbold.ttf', max_size = 10000, centered = False):
    lines = textvalue.split('\n')
    curr_size =min(box_size[1]//len(lines), max_size)+1#plus 1 because 1 will always be subtracted
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
    if not centered:
        for i, text in enumerate(texts):
            surface.blit(text, (box_position[0], box_position[1]+(curr_size*i)))
    else:
        for i, text in enumerate(texts):
            surface.blit(text, (box_position[0]+((box_size[0]/2)-(text.get_rect().width/2)), box_position[1]+(curr_size*i)+((box_size[1]-(curr_size * len(texts)))/2)))