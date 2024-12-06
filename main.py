import pygame
import numpy as np

Width, Height = 800, 600

def init_goal():
    min_vert, max_vert = 4, 10
    min_area, max_area = 500, 4500
    target_vertices = np.random.randint(min_vert, max_vert)
    target_area = int(min_area + (max_area - min_area)*np.random.rand())
    return target_vertices, target_area

def display_goal(screen, target_vertices, target_area):
    text = font.render(f'Number of Vertex: %d'%target_vertices, True, (255, 255, 255))
    screen.blit(text, (Width-350 , Height-100))
    text = font.render(f'Target Area: %d'%target_area, True, (255, 255, 255))
    screen.blit(text, (Width-350 , Height-50))

def display_area(screen, xy):
    text = font.render(f'%.1f'%area(xy), True, (255, 255, 255))
    screen.blit(text, (20, 5))

def area(xy):
    xy = np.array(xy)/10
    xy -= np.array([40, 30])
    sum = 0
    for i in range(len(xy)):
        sum += xy[i][0]*xy[(i+1)%len(xy)][1] - xy[i][1]*xy[(i+1)%len(xy)][0]
    return abs(sum)/2

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((Width, Height))

play, num_vertices, xy = True, 0, []
target_vertices, target_area = init_goal()
display_goal(screen, target_vertices, target_area)

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.button) # 1:left 2:middle 3:right
            if event.button == 1:
                num_vertices += 1
                x, y = pygame.mouse.get_pos()
                xy.append((x, y))
                pygame.draw.circle(screen, (255, 255, 255), (x, y), 3)
            if event.button == 3:
                pygame.draw.polygon(screen, (255, 255, 255), xy)
                display_area(screen, xy)
            if event.button == 2:
                screen.fill((0, 0, 0))
                num_vertices, xy = 0, []
                target_vertices, target_area = init_goal()
                display_goal(screen, target_vertices, target_area)
    pygame.display.flip()

pygame.quit()