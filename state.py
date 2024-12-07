import pygame
import numpy as np
from ui import UI



class State:
    def __init__(self, screen, font, Width, Height, shape, draw):
        self.state = "START"
        self.state_list = ["START", "CHECK", "DRAW", "GAMEOVER"]
        self.screen = screen
        self.font = font
        self.width = Width
        self.height = Height
        self.shape = shape
        self.draw = draw

        # text
        self.start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        self.end_text = self.font.render("GAME OVER press SPACE to restart", True, (255, 255, 255))

        # start screen
        self.reset()

        

    def __eq__(self, other):
        if isinstance(other, str):
            return self.state == other
    
    def __repr__(self):
        return f"State({self.state})"
    
    def reset(self):
        self.screen.fill((0, 0, 0))
        if self.state == "START":
            self.screen.blit(self.start_text, (self.width // 2 - 150, self.height // 2))
        if self.state == "CHECK":
            pass
        if self.state == "DRAW":
            pass
        if self.state == "GAMEOVER":
            self.screen.blit(self.end_text, (self.width // 2 - 250, self.height // 2))

    def change_state(self, other):
        if isinstance(other, str) and other in self.state_list:
            self.state = other
            self.reset()

    def print_draw_area(self):
        area = self.draw.area()
        text = self.font.render(f'Area: %d'%area, True, (255, 255, 255))
        self.screen.blit(text, (20 , 15))

"""
    def update_draw(self, draw):
        self.draw = draw

    def update_shape(self, shape):
        self.shape = shape
"""