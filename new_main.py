import pygame
import numpy as np
from shape import Shape
from draw import Draw
from state import State

# 게임 설정
Width, Height = 800, 600
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()

# 상태 플래그
state = State(screen, font, Width, Height)

# 게임 루프
running = True
current_shape = Shape()
current_draw = Draw(screen)



while running:

    current_shape.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if (state == "START" or state == "GAMEOVER") and event.key == pygame.K_SPACE:
                state.change_state("DRAW")
                current_shape.generate_random_shape()

            # GAMEOVER DEBUG
            if event.key == pygame.K_0:
                state.change_state("GAMEOVER")
                

        if state == "DRAW":
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
