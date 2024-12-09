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
                

        if state == "CHECK":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [1,2,3]:
                    print(click_type[event.button-1]) 
                if event.button == 2:
                    state.reset()
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    current_draw.node_add(x, y)
                if event.button == 3:
                    if current_draw.finish_shape():
                        state.print_draw_area()
        elif state == "DRAW":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [0,1,2]:
                    print(click_type[event.button-1]) 
                if event.button == 2:
                    state.reset()
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    current_draw.node_add(x, y)
                if event.button == 3:
                    if current_draw.finish_shape():
                        state.print_draw_area()
                        current_shape.draw(screen)
        elif state == "MONEY":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [0,1,2]:
                    print(click_type[event.button-1]) 
                if event.button == 2:
                    state.reset()
            

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
