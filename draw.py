import pygame
import numpy as np
from shape import Edge

class Draw:
    def __init__(self, screen, color = (255, 255, 255), width = 3, ui = None):
        self.screen = screen
        self.node = []
        self.edge = []
        self.color = color
        self.width = width
        self.finished =False
        self.ui = ui

    def node_add(self, x, y):
        p1 = (x, y)
        
        if(len(self.node) > 0):
            p2 = self.node[-1]
            e = Edge(p1, p2)
            if self.check_edge(e):
                self.edge.append(e)
                pygame.draw.line(self.screen, self.color, p1, p2, self.width)
            else:
                print("[Error] Edge is intersecting!")
                return
        
        self.node.append(p1)
        pygame.draw.circle(self.screen, self.color, p1, self.width)

    def check_edge(self, e1):
        for e2 in self.edge[:-1]:
            if e1.is_intersecting(e2):
                return False
        return True

    def finish_shape(self):
        if len(self.node) <3:
            print("[Error] Shape not finished!")
            return
        p1 = self.node[0]; p2 = self.node[-1]
        e1 = Edge(p1, p2)
        for e2 in self.edge[1:-1]:
            if e1.is_intersecting(e2):
                print("[Error] Last edge is intersecting!")
                return
        self.edge.append(e1)
        pygame.draw.polygon(self.screen, self.color, self.node)
        self.finished = True

    def reset(self):
        self.node = []
        self.edge = []
        self.finished =False
        #self.ui.draw()
