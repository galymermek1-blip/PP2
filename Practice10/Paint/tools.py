import pygame
import math


def draw_line(surface, color, start, end, size):
    pygame.draw.line(surface, color, start, end, size)


def draw_rectangle(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(surface, color, rect, size)


def draw_circle(surface, color, start, end, size):
    radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
    pygame.draw.circle(surface, color, start, radius, size)


def draw_square(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x1 -= side
    if y2 < y1:
        y1 -= side

    rect = pygame.Rect(x1, y1, side, side)
    pygame.draw.rect(surface, color, rect, size)


def draw_right_triangle(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x2, y2), (x1, y2)]
    pygame.draw.polygon(surface, color, points, size)


def draw_equilateral_triangle(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)
    direction = 1 if x2 >= x1 else -1

    p1 = (x1, y1)
    p2 = (x1 + side * direction, y1)
    p3 = (x1 + (side // 2) * direction, y1 - int(side * 0.866))

    pygame.draw.polygon(surface, color, [p1, p2, p3], size)


def draw_rhombus(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
    pygame.draw.polygon(surface, color, points, size)


def draw_shape(surface, tool, color, start, end, size):
    if tool == "line":
        draw_line(surface, color, start, end, size)
    elif tool == "rect":
        draw_rectangle(surface, color, start, end, size)
    elif tool == "circle":
        draw_circle(surface, color, start, end, size)
    elif tool == "square":
        draw_square(surface, color, start, end, size)
    elif tool == "rtriangle":
        draw_right_triangle(surface, color, start, end, size)
    elif tool == "etriangle":
        draw_equilateral_triangle(surface, color, start, end, size)
    elif tool == "rhombus":
        draw_rhombus(surface, color, start, end, size)


def flood_fill(surface, start_pos, fill_color, ui_height):
    target_color = surface.get_at(start_pos)

    if target_color == fill_color:
        return

    width, height = surface.get_size()
    stack = [start_pos]

    while stack:
        x, y = stack.pop()

        if x < 0 or x >= width or y < ui_height or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))
def draw_shape(surface, tool, color, start, end, size):
    if tool == "line":
        draw_line(surface, color, start, end, size)

    elif tool == "rect":
        draw_rectangle(surface, color, start, end, size)

    elif tool == "circle":
        draw_circle(surface, color, start, end, size)

    elif tool == "square":
        draw_square(surface, color, start, end, size)

    elif tool == "rtriangle":
        draw_right_triangle(surface, color, start, end, size)

    elif tool == "etriangle":
        draw_equilateral_triangle(surface, color, start, end, size)

    elif tool == "rhombus":
        draw_rhombus(surface, color, start, end, size)    