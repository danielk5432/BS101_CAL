import numpy as np
import pygame

class Shape:
    def __init__(self):
        self.vertices = []
        self.area = 0

    def generate_random_shape(self):
        shapes = ["triangle", "square", "rectangle", "pentagon", "star"]
        self.type = np.random.choice(shapes)

        # 중심과 크기 설정
        center_x, center_y = np.random.randint(100, 700), np.random.randint(100, 500)
        size = np.random.randint(50, 100)

        if self.type == "triangle":
            self.vertices = [
                (center_x, center_y - size),
                (center_x - size, center_y + size),
                (center_x + size, center_y + size),
            ]
        elif self.type == "square":
            self.vertices = [
                (center_x - size, center_y - size),
                (center_x + size, center_y - size),
                (center_x + size, center_y + size),
                (center_x - size, center_y + size),
            ]
        elif self.type == "rectangle":
            self.vertices = [
                (center_x - size, center_y - size // 2),
                (center_x + size, center_y - size // 2),
                (center_x + size, center_y + size // 2),
                (center_x - size, center_y + size // 2),
            ]
        elif self.type == "pentagon":
            angle = np.linspace(0, 2 * np.pi, 6)
            self.vertices = [(center_x + size * np.cos(a), center_y + size * np.sin(a)) for a in angle[:-1]]
        elif self.type == "star":
            self.vertices = [
                (center_x, center_y - size),
                (center_x + size // 2, center_y - size // 3),
                (center_x + size, center_y),
                (center_x + size // 3, center_y + size // 2),
                (center_x + size // 2, center_y + size),
                (center_x, center_y + size // 3),
                (center_x - size // 2, center_y + size),
                (center_x - size // 3, center_y + size // 2),
                (center_x - size, center_y),
                (center_x - size // 2, center_y - size // 3),
            ]

    def draw(self, screen):
        if len(self.vertices) > 2:
            pygame.draw.polygon(screen, (0, 255, 0), self.vertices, 2)
