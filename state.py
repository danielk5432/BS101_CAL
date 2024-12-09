import pygame
import numpy as np
from ui import UI



class State:
    def __init__(self, screen, font, Width, Height, shape, draw, check_try):
        self.state = "START"
        self.state_list = ["START", "CHECK", "DRAW", "ADJUSTMENT", "GAMEOVER"]
        self.screen = screen
        self.font = font
        self.width = Width
        self.height = Height
        self.shape = shape
        self.draw = draw
        self.max_check_try = check_try
        self.check_try = 0
        self.ui = UI(screen, font, Width, Height, self)
        self.money = 1000
        self.round = 1

        # start screen
        self.reset()
    
    def new_game(self):
        self.check_try = 0
        self.money = 1000
        self.round = 1

    def get_state(self):
        return self.state

    def __eq__(self, other):
        if isinstance(other, str):
            return self.state == other
    
    def __repr__(self):
        return f"State({self.state})"
    
    def reset(self):
        
        if self.state == "START":
            pass
        if self.state == "CHECK":
            self.draw.reset()
            if self.check_left() == 0:
                self.change_state("DRAW")
        if self.state == "DRAW":
            self.draw.reset()
        if self.state == "GAMEOVER":
            pass
        if self.state == "ADJUSTMENT":
            pass
        self.ui.update()
    def change_state(self, other):
        if isinstance(other, str) and other in self.state_list:
            self.state = other
            if self.state == "ADJUSTMENT":
                return
            self.reset()

    def print_draw_area(self):
        self.ui.print_draw_area(self.draw, self.shape)
        self.check_try += 1
    
    def check_left(self):
        return self.max_check_try - self.check_try
"""
    def update_draw(self, draw):
        self.draw = draw

    def update_shape(self, shape):
        self.shape = shape
"""