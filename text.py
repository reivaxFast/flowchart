import pygame
def return_lines_in_a_box(textvalue: str, box_size: tuple, max_size = 10000, min_size = 10, numbered = False):
    if len(textvalue) == 0 and numbered:
        numbered = False
        textvalue = '1'
    lines = textvalue.split('\n')
    if len(textvalue) != 0:
        if numbered:
            lines = [str(i+1) + ' ' + j for i, j in enumerate(lines)]
        #print(lines)
        curr_size =min(box_size[1]//len(lines), max_size)+1#plus 1 because 1 will always be subtracted
        largest_x = box_size[0]+1
        text_type = 'fonts/Cascadia.ttf'
        while largest_x > box_size[0]:
            font = pygame.font.Font(text_type, curr_size)
            ind_size = font.render('a', True, (255, 255, 255)).get_rect().width #all charecters are the same size
            #print(font.render('a', True, (255, 255, 255)).get_rect().height)
            largest_x = 0
            curr_size -= 1
            if curr_size + 1 < max(2, min_size):
                break
            for i in lines:
                curr_x = ind_size * len(i)
                if curr_x > largest_x:
                    largest_x = curr_x
        #print(lines, curr_size)
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
                        lines.insert(largest_x_index, '  '+line[i:])
                        lines.insert(largest_x_index, line[:i])
                        run = True
                        break
        print(curr_size)
        return lines, curr_size, len(lines) * curr_size > box_size[1]
    else:
        return [''], 10, False

def render_text_in_box(lines: list, surface: pygame.Surface, box_position: tuple, box_size: tuple, size, colour = (0,0,0), centered = False):
    if len(''.join(lines)) != 0:
        text_type = 'fonts/Cascadia.ttf'
        font = pygame.font.Font(text_type, size)
        texts = [font.render(x, True, colour) for x in lines]
        if not centered:
            for i, text in enumerate(texts):
                surface.blit(text, (box_position[0], box_position[1]+(size*i)))
        else:
            for i, text in enumerate(texts):
                surface.blit(text, (box_position[0]+((box_size[0]/2)-(text.get_rect().width/2)), box_position[1]+(size*i)+((box_size[1]-(size * len(texts)))/2)))