import pygame
def get_line_positions(start: tuple, end: tuple, width = 200):
    half_width = width / 2
    li = [start]
    if start[1] + 20 > end[1]:
        if start[0] < end[0] + width +20 and start[0]  + width + 20 > end[0]:
            li.append((start[0], start[1]+10))
            if start[0] > end[0]:
                li.append(((start[0] - (half_width+10)), start[1]+10))
                li.append(((start[0] - (half_width+10)), (start[1]+end[1])/2))
                li.append(((end[0] + (half_width+10)), (start[1]+end[1])/2))
                li.append(((end[0] + (half_width+10)), end[1]-10))
            else:
                li.append(((start[0] + (half_width+10)), start[1]+10))
                li.append(((start[0] + (half_width+10)), (start[1]+end[1])/2))
                li.append(((end[0] - (half_width+10)), (start[1]+end[1])/2))
                li.append(((end[0] - (half_width+10)), end[1]-10))
            li.append((end[0], end[1]-10))
        else:
            li.append((start[0], start[1]+10))
            li.append(((start[0]+end[0])/2, start[1]+10))
            li.append(((start[0]+end[0])/2, end[1]-10))
            li.append((end[0], end[1]-10))
    else:
        li.append((start[0], (start[1]+end[1])/2))
        li.append((end[0], (start[1]+end[1])/2))
    li.append(end)
    return li

def draw_line(boxes: list, indexs: tuple, boxes_index: list, window:pygame.Surface, width: int = 10, box_width = 200):
    win = window
    index1 = boxes_index.index(indexs[0])
    start = (boxes[index1].x+(boxes[index1].w/2), boxes[index1].y + boxes[index1].h)
    if indexs[1] != -1:
        index2 = boxes_index.index(indexs[1])
        end = (boxes[index2].x + (boxes[index2].w/2), boxes[index2].y)
    else:
        end = pygame.mouse.get_pos()
    
    points = get_line_positions(start, end, box_width)
    for i in points[1:-1]:
        pygame.draw.circle(win, (255, 255, 255), (i[0]+1, i[1]+1), (width/2))
    pygame.draw.lines(win, (255, 255, 255), False, points, width)
    