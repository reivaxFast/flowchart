import pygame
def get_line_positions(start: tuple, end: tuple, width1 = 200, width2 = 200, if2 = False, h1 = 50):
    half_width1 = width1 / 2
    half_width2 = width2 / 2
    ave_W = half_width1 + half_width2
    li = []
    if not if2:
        li = [(start[0], start[1]-20)]
        if ((start[1] + 20 > end[1] and width2 != 0) or (start[1] + 10 > end[1] and width2 == 0)) and (not 20 > end[1] - start[1] > -20 or abs(end[0]-start[0]) >ave_W + 20):
            if ((start[0] < end[0] + ave_W +20 and start[0]  + ave_W + 20 > end[0] and width2 != 0) or (start[0] < end[0] + half_width1 + 10 and start[0]  + half_width1 + 10> end[0] and width2 == 0)):
                li.append((start[0], start[1]+10))
                if start[0] > end[0]:
                    li.append(((start[0] - (half_width1+10)), start[1]+10))
                    li.append(((start[0] - (half_width1+10)), (start[1]+end[1])/2))
                    if width2 != 0:
                        li.append(((end[0] + (half_width2+10)), (start[1]+end[1])/2))
                        li.append(((end[0] + (half_width2+10)), end[1]-10))
                else:
                    li.append(((start[0] + (half_width1+10)), start[1]+10))
                    li.append(((start[0] + (half_width1+10)), (start[1]+end[1])/2))
                    if width2 != 0:
                        li.append(((end[0] - (half_width2+10)), (start[1]+end[1])/2))
                        li.append(((end[0] - (half_width2+10)), end[1]-10))
                if width2 != 0:
                    li.append((end[0], end[1]-10))
                else:
                    li.append((end[0], (start[1]+end[1])/2))
            else:
                li.append((start[0], start[1]+10))
                if end[0]>start[0]:
                    li.append((max((start[0]+end[0])/2, start[0] + half_width1 + 10), start[1]+10))
                    li.append((max((start[0]+end[0])/2, start[0] + half_width1 + 10), end[1]-(10 * (width2 != 0))))
                else:
                    li.append((min((start[0]+end[0])/2, start[0] - (half_width1 + 10)), start[1]+10))
                    li.append((min((start[0]+end[0])/2, start[0] - (half_width1 + 10)), end[1]-(10 * (width2 != 0))))
                if width2 != 0:
                    li.append((end[0], end[1]-10))
        else:
            if width2 != 0:
                li.append((start[0], (start[1]+end[1])/2))
                li.append((end[0], (start[1]+end[1])/2))
            else:
                li.append((start[0], max((start[1]+end[1])/2, start[1] + 10)))
                li.append((end[0], max((start[1]+end[1])/2, start[1] + 10)))
        if width2 != 0:
            li.append((end[0], end[1]+20))
        else:
            li.append(end)
    else:
        if start[0] > end[0]:
            li = [(start[0]-half_width1+20, start[1]-(h1/2))]
        else:
            li = [(start[0]+half_width1-20, start[1]-(h1/2))]
        if li[0][1] < end[1]-10:
            if end[0] < start[0] + half_width1 + 10 and end[0] > start[0] - half_width1 - 10:
                if start[0] > end[0]:
                    li.append((li[0][0]-30, li[0][1]))
                    li.append((li[0][0]-30, (li[0][1]+end[1])/2))
                    li.append((end[0], (li[0][1]+end[1])/2))
                else:
                    li.append((li[0][0]+30, li[0][1]))
                    li.append((li[0][0]+30, (li[0][1]+end[1])/2))
                    li.append((end[0], (li[0][1]+end[1])/2))
            else:
                li.append((end[0], li[0][1]))
        else:
            if end[0] + half_width1 + 20 > li[0][0] and end[0] < start[0]:
                li.append((end[0]-half_width2-10, li[0][1]))
                li.append((end[0]-half_width2-10, end[1]-10))
                li.append((end[0], end[1]-10))
            elif end[0] - half_width1 - 20 <= li[0][0] and end[0] >= start[0]:
                li.append((end[0]+half_width2+10, li[0][1]))
                li.append((end[0]+half_width2+10, end[1]-10))
                li.append((end[0], end[1]-10))
            elif end[0] < start[0]:
                li.append((((end[0]+half_width2)+li[0][0])/2, li[0][1]))
                li.append((((end[0]+half_width2)+li[0][0])/2, end[1]-10))
                li.append((end[0], end[1]-10))
            else:
                li.append((((end[0]-half_width2)+li[0][0])/2, li[0][1]))
                li.append((((end[0]-half_width2)+li[0][0])/2, end[1]-10))
                li.append((end[0], end[1]-10))
        li.append(end)
    return li

def draw_line(boxes: list, indexs: tuple, boxes_index: list, win:pygame.Surface, width: int = 10, if2 = False):
    index1 = boxes_index.index(indexs[0])
    start = (boxes[index1].x+(boxes[index1].w/2), boxes[index1].y + boxes[index1].h)
    width1 = boxes[index1].w
    if indexs[1] != -1:
        index2 = boxes_index.index(indexs[1])
        end = (boxes[index2].x + (boxes[index2].w/2), boxes[index2].y)
        width2 = boxes[index2].w
    else:
        end = pygame.mouse.get_pos()
        width2 = 0
    
    points = get_line_positions(start, end, width1, width2, if2, boxes[index1].h)
    for i in points[1:-1]:
        pygame.draw.circle(win, (255, 255, 255), (i[0]+1, i[1]+1), (width/2))
    if width2 == 0:
        pygame.draw.circle(win, (255, 255, 255), (end[0]+1, end[1]+1), (width/2))
    pygame.draw.lines(win, (255, 255, 255), False, points, width)

def get_lines_hitbox(boxes, boxes_connections, boxes_index):
    points = []
    for i in boxes_connections:
        if i[1] != -1:
            index1 = boxes_index.index(i[0])
            start = (boxes[index1].x+(boxes[index1].w/2), boxes[index1].y + boxes[index1].h)
            width1 = boxes[index1].w
            index2 = boxes_index.index(i[1])
            end = (boxes[index2].x + (boxes[index2].w/2), boxes[index2].y)
            width2 = boxes[index2].w
            points.append(get_line_positions(start, end, width1, width2)[0])

def display_lines(window, boxes, boxes_connections, boxes_index):
    occured = []
    for i in boxes_connections:
        draw_line(boxes, i, boxes_index, window, 10, i[0] in occured)
        occured.append(i[0])