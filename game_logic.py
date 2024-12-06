import numpy as np
import pygame

Width, Height = 800, 600

def init_goal():
    min_vert, max_vert = 4, 10
    min_area, max_area = 500, 4500
    target_vertices = np.random.randint(min_vert, max_vert)
    target_area = int(min_area + (max_area - min_area) * np.random.rand())
    return target_vertices, target_area

def display_goal(screen, target_vertices, target_area, font, Width, Height):
    text = font.render(f'Number of Vertex: {target_vertices}', True, (255, 255, 255))
    screen.blit(text, (Width - 350, Height - 100))
    text = font.render(f'Target Area: {target_area}', True, (255, 255, 255))
    screen.blit(text, (Width - 350, Height - 50))

def display_area(screen, xy, font):
    calculated_area = area(xy)
    text = font.render(f'Area: {calculated_area:.1f}', True, (255, 255, 255))
    screen.blit(text, (20, 5))

def area(xy):
    xy = np.array(xy) / 10
    xy -= np.array([40, 30])
    total_area = 0
    for i in range(len(xy)):
        total_area += xy[i][0] * xy[(i + 1) % len(xy)][1] - xy[i][1] * xy[(i + 1) % len(xy)][0]
    return abs(total_area) / 2
