import pygame, math, keyboard

KEYS =         ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", '#', '\\', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '/', '*', '+', 'del', 'enter', 'backspace', 'space','.']
SHIFTED_KEYS = ['!', '"', '£', '$', '%', '^', '&', '*', '(', ')', '_', '+', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '@', '~',  '|', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?']
def return_lines_in_a_box(textvalue: str, box_size: tuple, max_size = 10000, min_size = 10, numbered = False, box_type = 'pro'):
    box_size = (box_size[0], box_size[1]-10)
    if len(textvalue) == 0 and numbered:
        numbered = False
        textvalue = '1'
    resize_value = 0
    minus = 0
    if box_type == 'io':
        resize_value = 0.5
        minus = math.ceil(box_size[1]*0.5)
    lines = textvalue.split('\n')
    if len(textvalue) != 0:
        if numbered:
            lines = [str(i+1) + ' ' + j for i, j in enumerate(lines)]
        curr_size =min(box_size[1]//len(lines), max_size)+1#plus 1 because 1 will always be subtracted
        largest_x = box_size[0]+1
        text_type = 'fonts/Cascadia.ttf'
        new_size = box_size[0] - math.ceil(curr_size*resize_value) - minus
        while largest_x > new_size:
            font = pygame.font.Font(text_type, curr_size)
            ind_size = font.render('a', True, (255, 255, 255)).get_rect().width #all charecters are the same size
            new_size = box_size[0] - round(curr_size*resize_value) - minus
            largest_x = 0
            curr_size -= 1
            if curr_size + 1 < max(2, min_size):
                break
            for i in lines:
                curr_x = ind_size * len(i)
                if curr_x > largest_x:
                    largest_x = curr_x
        if curr_size < min_size:
            curr_size = min_size
            font = pygame.font.Font(text_type, curr_size)
            run = True
            new_size = box_size[0] - math.ceil(curr_size*resize_value) - minus
            while run:
                run = False
                largest_x = 0
                for i in lines:
                    curr_x = len(i) * ind_size
                    if curr_x > new_size:
                        largest_x_index=lines.index(i)
                        line = lines.pop(largest_x_index)
                        i = new_size//ind_size
                        if numbered:
                            lines.insert(largest_x_index, '  '+line[i:])
                        else:
                            lines.insert(largest_x_index, ' '+line[i:])
                        lines.insert(largest_x_index, line[:i])
                        run = True
                        break
        return lines, curr_size, len(lines) * curr_size > box_size[1]
    else:
        return [''], 10, False

def render_text_in_box(lines: list, surface: pygame.Surface, box_position: tuple, box_size: tuple, size, colour = (0,0,0), centered = False, box_type = 'pro'):
    if len(''.join(lines)) != 0:
        text_type = 'fonts/Cascadia.ttf'
        font = pygame.font.Font(text_type, size)
        texts = [font.render(x, True, colour) for x in lines]
        if not box_type in ['io', 'if']:
            if not centered:
                for i, text in enumerate(texts):
                    surface.blit(text, (box_position[0], box_position[1]+(size*i)))
            else:
                for i, text in enumerate(texts):
                    surface.blit(text, (box_position[0]+((box_size[0]/2)-(text.get_rect().width/2)), box_position[1]+(size*i)+(((box_size[1]-(size * len(texts)))-(size/2))/2)))
        elif box_type == 'io':
            start_offset = math.ceil(box_size[1]*0.5)
            line_offset = math.ceil(size*0.5)
            for i, text in enumerate(texts):
                surface.blit(text, (box_position[0] + (start_offset-(line_offset*i)), box_position[1]+(size*i)))
        else:
            text = texts[0]
            ind_size = font.render('a', True, (255, 255, 255)).get_rect().width
            margin = ((box_size[0]/box_size[1])*((size/2)+5))
            largest_len = int((box_size[0]-(margin*2))//ind_size)
            if len(lines[0])>largest_len:
                text = font.render(lines[0][:largest_len-3]+'...', True, colour)
            surface.blit(text, (box_position[0]+margin, box_position[1]+(box_size[1]//2)-(size//2)))


def get_pressed_keys():
    ret = []
    if keyboard.is_pressed('shift'):
        for i in SHIFTED_KEYS:
            if keyboard.is_pressed(i):
                ret.append(i)
    else:
        for i in KEYS:
            if keyboard.is_pressed(i):
                if not i in ['*', '+', '.']:
                    if i == 'enter':
                        ret.append('\n')
                    elif i == 'space':
                        ret.append(' ')
                    else:
                        ret.append(i)
                else:
                    if not ('=' in ret or '8' in ret or 'del' in ret):
                        ret.append(i)
    return ret