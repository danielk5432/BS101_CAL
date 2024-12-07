import pygame
import numpy as np
import state as State

class UI:
    def __init__(self, screen, font, Width, Height, state):
        self.state_obj = state
        self.state = state.get_state()
        self.screen = screen
        self.font = font
        self.width = Width
        self.height = Height

        self.start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        self.end_text = self.font.render("GAME OVER press SPACE to restart", True, (255, 255, 255))

    def update(self):
        self.state_update()
        self.screen.fill((0, 0, 0))
        if self.state == "START":
            self.screen.blit(self.start_text, (self.width // 2 - 150, self.height // 2))
            
        if self.state == "CHECK":

            text = self.font.render(f"try left: {self.state_obj.max_check_try-self.state_obj.check_try}", True, (255, 255, 255))
            self.screen.blit(text, (self.width -150, 5))

        if self.state == "DRAW":
            pass
        if self.state == "GAMEOVER":
            self.screen.blit(self.end_text, (self.width // 2 - 250, self.height // 2))
    
    def state_update(self):
        self.state = self.state_obj.get_state()

    def print_draw_area(self, draw, shape):
        area = draw.area()
        intersect_area = draw.intersect_area(shape)
        text = self.font.render(f'Area: %d'%area, True, (255, 255, 255))
        self.screen.blit(text, (20 , 5))
        text = self.font.render(f'Intersect Area: %d'%intersect_area, True, (255, 255, 255))
        self.screen.blit(text, (20 , 50))