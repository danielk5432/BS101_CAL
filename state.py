import pygame
import numpy as np
from ui import UI



class State:
    def __init__(self, screen, font, Width, Height):
        self.state = "START"
        self.state_list = ["START", "CHECK", "DRAW", "GAMEOVER"]
        #self.ui = UI(screen)
        self.screen = screen
        self.font = font
        self.width = Width
        self.height = Height

        # text
        self.start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        self.end_text = self.font.render("GAME OVER press SPACE to restart", True, (255, 255, 255))

        # start screen
        screen.blit(self.start_text, (Width // 2 - 150, Height // 2))

        

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