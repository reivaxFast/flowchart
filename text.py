import pygame

def render_text_in_box(textvalue: str, surface: pygame.Surface, box_position: tuple, box_size: tuple, colour = (0,0,0), max_size = 10000, centered = False, min_size = 10):
    lines = textvalue.split('\n')
    curr_size =min(box_size[1]//len(lines), max_size)+1#plus 1 because 1 will always be subtracted
    largest_x = box_size[0]+1
    text_type = 'fonts/Cascadia.ttf'
    if len(textvalue) != 0:
        while largest_x > box_size[0]:
            font = pygame.font.Font(text_type, curr_size)
            ind_size = font.render('a', True, (255, 255, 255)).get_rect().width #all charecters are the same size
            largest_x = 0
            curr_size -= 1
            if curr_size + 1 < max(2, min_size):
                break
            for i in lines:
                curr_x = ind_size * len(i)
                if curr_x > largest_x:
                    largest_x = curr_x
        curr_size += 1
        if curr_size < min_size:
            curr_size = min_size
            font = pygame.font.Font(text_type, curr_size)
            run = True
            while run:
                run = False
                largest_x = 0
                for i in lines:
                    curr_x = len(i) * ind_size
                    if curr_x > box_size[0]:
                        largest_x_index=lines.index(i)
                        line = lines.pop(largest_x_index)
                        i = box_size[0]//ind_size
                        lines.insert(largest_x_index, line[i:])
                        lines.insert(largest_x_index, line[:i])
                        run = True
                        break
        font = pygame.font.Font(text_type, curr_size)
        texts = [font.render(x, True, colour) for x in lines]
        if not centered:
            for i, text in enumerate(texts):
                surface.blit(text, (box_position[0], box_position[1]+(curr_size*i)))
        else:
            for i, text in enumerate(texts):
                surface.blit(text, (box_position[0]+((box_size[0]/2)-(text.get_rect().width/2)), box_position[1]+(curr_size*i)+((box_size[1]-(curr_size * len(texts)))/2)))