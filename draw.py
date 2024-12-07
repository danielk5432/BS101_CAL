import pygame
import numpy as np

class Draw:
    def __init__(self, screen, color = (255, 255, 255), width = 3, ui = None):
        self.screen = screen
        self.node = []
        self.color = color
        self.width = width
        self.finished =False
        self.ui = ui

    def node_add(self, x, y):
        self.node.append((x,y))
        pygame.draw.circle(self.screen, self.color, (x, y), self.width)
        print(self.color)
        if(len(self.node) > 1):
            pygame.draw.line(self.screen, self.color, (x, y), self.node[-1], self.width)

    def finish_shape(self):
        if len(self.node) <3:
            print("[Error] Shape not finished!")
            return
        pygame.draw.polygon(self.screen, self.color, self.node)
        self.finished = True

    def reset(self):
        self.screen.fill((0, 0, 0))
        self.node = []
        #self.ui.draw()
