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
draw_try = 5

# Debug
click_type = ["Left Click", "Middle Click", "Right Click"]

# 게임 루프
running = True
current_shape = Shape(screen)
current_draw = Draw(screen)

state = State(screen, font, Width, Height, current_shape, current_draw, draw_try)
mouse_down = False
while running:

    #current_shape.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if (state == "START" or state == "GAMEOVER") and event.key == pygame.K_SPACE:
                state.new_game()
                state.change_state("CHECK")
                current_shape.generate_random_shape()

            # GAMEOVER DEBUG
            if event.key == pygame.K_0:
                state.change_state("GAMEOVER")
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and state in ["CHECK", "DRAW", "MONEY"]:
            state.reset()

        if state == "CHECK":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [1,2,3]:
                    print(click_type[event.button-1]) 
                if event.button == 2 or current_draw.finished:
                    state.reset()
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    mouse_down = True
                    current_draw.node_add(x, y)
                if event.button == 3:
                    if current_draw.finish_shape():
                        state.print_draw_area()
            elif event.type == pygame.MOUSEMOTION:
                if mouse_down:  # 왼쪽 버튼을 누른 상태에서 움직임
                    x, y = pygame.mouse.get_pos()
                    current_draw.node_add(x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 왼쪽 버튼에서 손 뗌
                    mouse_down = False
        elif state == "DRAW":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [0,1,2]:
                    print(click_type[event.button-1]) 
                if event.button == 2 or current_draw.finished:
                    state.reset()
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    mouse_down = True
                    current_draw.node_add(x, y)
                if event.button == 3:
                    if current_draw.finish_shape():
                        state.print_draw_area()
                        current_shape.draw(screen)
            elif event.type == pygame.MOUSEMOTION:
                if mouse_down:  # 왼쪽 버튼을 누른 상태에서 움직임
                    x, y = pygame.mouse.get_pos()
                    current_draw.node_add(x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 왼쪽 버튼에서 손 뗌
                    mouse_down = False
        elif state == "MONEY":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [0,1,2]:
                    print(click_type[event.button-1])
                    state.reset()
            

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
