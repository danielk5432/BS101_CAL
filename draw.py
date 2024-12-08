import pygame
import numpy as np
from shape import Edge, Shape

class Draw:
    def __init__(self, screen, color = (255, 255, 255), width = 3):
        self.screen = screen
        self.node = []
        self.edge = []
        self.shape = Shape(screen)
        self.color = color
        self.width = width
        self.finished =False

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
            return False
        p1 = self.node[0]; p2 = self.node[-1]
        e1 = Edge(p1, p2)
        for e2 in self.edge[1:-1]:
            if e1.is_intersecting(e2):
                print("[Error] Last edge is intersecting!")
                return False
        self.edge.append(e1)
        self.shape.generate_user_shape(self.node)
        self.shape.draw(self.screen, self.color)
        self.finished = True
        return True
    
    def area(self):
        return self.shape.get_area()
    
    def intersect_area(self, shape: 'Shape') -> float:
        intersection = self.shape.sutherland_hodgman_clip(shape)
        area = intersection.calculate_area()
        return area

    def reset(self):
        self.node = []
        self.edge = []
        self.finished =False
