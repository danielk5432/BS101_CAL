import numpy as np
import pygame
from typing import Tuple, List

class Edge:
    def __init__(self, p1: Tuple[float, float], p2: Tuple[float, float]):
        self.start_point = p1
        self.end_point = p2
    def get_start(self):
        return self.start_point
    def get_end(self):
        return self.end_point
    def get_pair(self):
        return self.start_point, self.end_point

    def draw(self, screen, color: Tuple[int, int, int]):
        pygame.draw.line(screen, color, self.start_point, self.end_point)

    def is_intersecting(self, e1: 'Edge'):
        def ccw(a, b, c):
            # CCW: 세 점이 시계/반시계 방향 여부를 판별
            # clockwise: True
            return (b[1] - a[1]) * (c[0] - a[0]) > (c[1] - a[1]) * (b[0] - a[0])

        p1, p2 = self.get_pair()
        q1, q2 = e1.get_pair()
        return (ccw(p1, p2, q1) != ccw(p1, p2, q2)) and (ccw(q1, q2, p1) != ccw(q1, q2, p2))


    def intersection_point(self, e1: 'Edge') -> Tuple[int, int]:
        p1, p2 = self.get_pair()
        q1, q2 = e1.get_pair()

        # 선분의 직선 방정식을 기반으로 계산
        a1, b1 = p2[1] - p1[1], p1[0] - p2[0]
        c1 = a1 * p1[0] + b1 * p1[1]
        
        a2, b2 = q2[1] - q1[1], q1[0] - q2[0]
        c2 = a2 * q1[0] + b2 * q1[1]
        
        determinant = a1 * b2 - a2 * b1
        
        if determinant == 0:
            # 평행한 경우, 교점 없음
            return None
        
        # 교점 좌표 계산
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        
        # 교점이 두 선분 위에 있는지 확인
        def is_on_segment(p, q, r):
            # 점 r이 선분 (p, q) 위에 있는지 확인
            return (min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and
                    min(p[1], q[1]) <= r[1] <= max(p[1], q[1]))
        
        if is_on_segment(p1, p2, (x, y)) and is_on_segment(q1, q2, (x, y)):
            return (x, y)
        return None



class Shape:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.area = 0

    def generate_random_shape(self):
        shapes = ["triangle", "square", "rectangle", "pentagon", "star"]
        #self.type = np.random.choice(shapes)
        self.type = "star"
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
            outer_radius = size
            inner_radius = outer_radius * np.sin(np.radians(18)) / np.cos(np.radians(36))  # 정오각형 별의 경우

            # 꼭짓점 계산
            self.vertices = [
                (center_x + outer_radius, center_y),  # 꼭짓점 1 (외곽)
                (center_x + inner_radius * np.sin(np.radians(54)), center_y - inner_radius * np.cos(np.radians(54))),  # 꼭짓점 2 (내부)
                (center_x + outer_radius * np.sin(np.radians(18)), center_y - outer_radius * np.cos(np.radians(18))),  # 꼭짓점 3 (외곽)
                (center_x + inner_radius * np.sin(np.radians(-18)), center_y - inner_radius * np.cos(np.radians(-18))),  # 꼭짓점 4 (내부)
                (center_x + outer_radius * np.sin(np.radians(-54)), center_y - outer_radius * np.cos(np.radians(-54))),  # 꼭짓점 5 (외곽)
                (center_x + inner_radius * np.sin(np.radians(-90)), center_y - inner_radius * np.cos(np.radians(-90))),  # 꼭짓점 6 (내부)
                (center_x + outer_radius * np.sin(np.radians(-126)), center_y - outer_radius * np.cos(np.radians(-126))),  # 꼭짓점 7 (외곽)
                (center_x + inner_radius * np.sin(np.radians(-162)), center_y - inner_radius * np.cos(np.radians(-162))),  # 꼭짓점 8 (내부)
                (center_x + outer_radius * np.sin(np.radians(-198)), center_y - outer_radius * np.cos(np.radians(-198))),  # 꼭짓점 9 (외곽)
                (center_x + inner_radius * np.sin(np.radians(-234)), center_y - inner_radius * np.cos(np.radians(-234))),  # 꼭짓점 10 (내부)
            ]

    def draw(self, screen):
        if len(self.vertices) > 2:
            pygame.draw.polygon(screen, (0, 255, 0), self.vertices, 2)

    def make_edge(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> 'Edge':
        e1 = Edge(p1, p2)
        self.edges.append(e1)
        return e1

    def make_edge_sequential(self, p_lst: Tuple[Tuple[float, float], ...] | List[Tuple[float, float]]) -> List['Edge']:
        l = len(p_lst)
        if (l < 2):
            return None
        edge_lst = []
        p = p_lst[0]
        q = p
        for i in range(l):
            q = p
            p = p_lst[i]
            edge_lst.append(Edge(p, q))
        self.edges.extend(edge_lst[1:])
        return edge_lst[1:]
        
    def get_intersections(self, new_edge: Edge|None = None) -> Tuple[List[Tuple[int, int]], List['Edge']] | None:
        if (len(self.edges) == 0):
            return None
        temp_edge_lst = self.edges.copy()
        temp_edge_lst.append(new_edge)
        intersections = []
        intersecting_edges = []
        e1 = temp_edge_lst[0]
        e2 = e1
        for i in range(len(temp_edge_lst)):
            e1 = temp_edge_lst[i]
            for j in range(i, len(temp_edge_lst)):
                e2 = temp_edge_lst[j]
                if (e1 is e2):
                    continue
                if (e1.is_intersecting(e2)):
                    intersections.append(e1.intersection_point(e2))
                    intersecting_edges.append((e1, e2))
        return intersections, intersecting_edges
    
    def get_vertices(self):
        return self.vertices.copy()