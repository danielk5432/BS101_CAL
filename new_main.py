import pygame
import numpy as np
from shape import Shape
from draw import Draw

# 게임 설정
Width, Height = 800, 600
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()

# 상태 플래그
START, CHECK, DRAW, GAMEOVER = 0, 1, 2, 3
state = START

# 게임 루프
running = True
current_shape = Shape()
current_draw = Draw(screen)

start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
screen.blit(start_text, (Width // 2 - 150, Height // 2))

while running:

    current_shape.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if (state == START or state == GAMEOVER) and event.key == pygame.K_SPACE:
                state = DRAW
                current_shape.generate_random_shape()
                screen.fill((0, 0, 0))

            # GAMEOVER DEBUG
            if event.key == pygame.K_0:
                state = GAMEOVER
                screen.fill((0, 0, 0))
                start_text = font.render("GAME OVER press SPACE to restart", True, (255, 255, 255))
                screen.blit(start_text, (Width // 2 - 200, Height // 2))

        if state == DRAW:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.button) # 1:left 2:middle 3:right
                if event.button == 2:
                    current_draw.reset()
                    screen.fill((0, 0, 0))
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    current_draw.node_add(x, y)
                if event.button == 3:
                    current_draw.finish_shape()
            

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
