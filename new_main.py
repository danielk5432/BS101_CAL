import pygame
import numpy as np
from shape import Shape

# 게임 설정
Width, Height = 800, 600
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()

# 상태 플래그
START, GAME = 0, 1
state = START

# 게임 루프
running = True
current_shape = Shape()

while running:
    screen.fill((0, 0, 0))

    if state == START:
        # 시작 화면
        text = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(text, (Width // 2 - 150, Height // 2))
    elif state == GAME:
        # 게임 화면
        current_shape.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and state == START:
                state = GAME
                current_shape.generate_random_shape()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
