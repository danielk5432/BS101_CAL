import pygame
import numpy as np
from ui import UI



class State:
    def __init__(self, screen, font, Width, Height, shape, draw, check_try, start_money = 200):
        self.state = "START"
        self.state_list = ["START", "CHECK", "DRAW", "MONEY", "GAMEOVER"]
        self.screen = screen
        self.font = font
        self.width = Width
        self.height = Height
        self.shape = shape
        self.draw = draw
        self.max_check_try = check_try
        self.check_try = 0
        self.ui = UI(screen, font, Width, Height, self)
        self.money = start_money
        self.start_money = start_money
        self.add_money = 0
        self.round = 1

        # start screen
        self.reset()
    
    def new_game(self):
        self.check_try = 0
        self.money = self.start_money
        self.round = 1

    def get_state(self):
        return self.state

    def __eq__(self, other):
        if isinstance(other, str):
            return self.state == other
    
    def __repr__(self):
        return f"State({self.state})"
    
    def reset(self):
        print("State Reset")
        if self.state == "START":
            pass
        elif self.state == "CHECK":
            self.draw.reset()
            if self.check_left() == 0:
                self.check_try = 0
                self.change_state("DRAW")
        elif self.state == "DRAW":
            self.draw.reset()

            # calculate money and print
            if self.draw.finished:
                intersect = self.draw.intersect_area(self.shape)
                area = self.draw.area()
                self.add_money = intersect * 2 - area
                self.ui.money_text = str(int(intersect)) + " * 2 - " + str(int(area)) + " = " + str(int(self.add_money)) + " money added"
                self.change_state("MONEY")
        elif self.state == "MONEY":
            self.money += self.add_money
            self.round += 1
            if self.money <= 0:
                self.change_state("GAMEOVER")
            else:
                self.shape.generate_random_shape()
                self.change_state("CHECK")
        elif self.state == "GAMEOVER":
            pass

        self.ui.update()

    def change_state(self, other):
        print("STATE CHANGE : " + self.state)
        if isinstance(other, str) and other in self.state_list:
            self.state = other
            self.ui.update()

    def print_draw_area(self):
        self.ui.print_draw_area(self.draw, self.shape)
        if self.state == "CHECK":
            self.check_try += 1
    
    def check_left(self):
        return self.max_check_try - self.check_try
    
    def change_money(self):
        pass
"""
    def update_draw(self, draw):
        self.draw = draw

    def update_shape(self, shape):
        self.shape = shape
"""