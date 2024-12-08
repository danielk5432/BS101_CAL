import numpy as np
import pygame
from typing import Tuple, List
from sutherland_hodgman import sutherland_hodgman_clip

class Edge:
    def __init__(self, p1: Tuple[float, float], p2: Tuple[float, float]):
        self.start_point = p1
        self.end_point = p2
    def __eq__(self, other: 'Edge'):
        return (self.start_point == other.start_point and self.end_point == other.end_point)
    def __repr__(self):
        return str(self)
    def __str__(self):
        return f'({self.start_point}, {self.end_point})'
    
    def get_start(self):
        return self.start_point
    def get_end(self):
        return self.end_point
    def get_pair(self):
        return self.start_point, self.end_point

    def draw(self, screen, color: Tuple[int, int, int], width: int):
        pygame.draw.line(screen, color, self.start_point, self.end_point, width)

    def is_intersecting(self, e1: 'Edge'):
        """현재 Edge가 주어진 Edge와 교차하는지 판별
        로직: 한쪽 Edge를 기준으로 다른 Edge의 두 점의 방향이 반대인지 확인, 그 반대도 확인
        두 Edge가 완전히 동일할 때: False
        두 Edge의 한쪽 끝점이 동일할 때: True
        모든 점이 일직선 상에 놓일 때: False"""
        def ccw(a, b, c):
            """세 점이 시계/반시계 방향 여부를 판별
            로직: 벡터 ab, ac의 외적(ab x ac)이 양수일 때 반시계, 외적이 음수일 때 시계, 외적이 0일 때 일직선상(두 점이 같은 경우 포함)
            counterclockwise: True, clockwise: False
            세 점이 직선 위에 놓일 때, 세 점 중 두 점이 동일할 때: False
            """
            return (b[1] - a[1]) * (c[0] - a[0]) - (c[1] - a[1]) * (b[0] - a[0]) > 0

        p1, p2 = self.get_pair()
        q1, q2 = e1.get_pair()
        return (ccw(p1, p2, q1) != ccw(p1, p2, q2)) and (ccw(q1, q2, p1) != ccw(q1, q2, p2))


    def intersection_point(self, e1: 'Edge') -> Tuple[float, float]:
        """현재 Edge가 주어진 Edge와 교차하면 교차점(Tuple[float, float]) 반환, 아니면 None 반환
        로직: 행렬식(determinant)을 이용해서 좌표 구함. 
              평행한지 확인(determinant==0), 평행하지 않다면 직선의 방정식으로 교점 구하기, 그 교점이 두 선분 사이에 있는지 확인"""
        p1, p2 = self.get_pair()
        q1, q2 = e1.get_pair()

        # 선분의 직선 방정식을 기반으로 계산
        # ax + by = c
        # AX = b (행렬 표현)
        a1, b1 = p2[1] - p1[1], p1[0] - p2[0]
        c1 = a1 * p1[0] + b1 * p1[1]
        
        a2, b2 = q2[1] - q1[1], q1[0] - q2[0]
        c2 = a2 * q1[0] + b2 * q1[1]
        
        determinant = a1 * b2 - a2 * b1
        
        if determinant == 0:
            # 평행 또는 동일한 경우, 교점 없음
            return None
        
        # 교점 좌표 계산
        # X = A^(-1)b (행렬 표현 / A^(-1)은 A의 역행렬)
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
    def __init__(self, screen):
        self.vertices = []
        self.edges = []
        self.area = 0
        self.screen = screen
    def get_vertices(self):
        return self.vertices.copy()
    def get_edges(self):
        return self.edges.copy()
    def get_area(self):
        return self.area

    def generate_random_shape(self):
        shapes = ["triangle", "square", "rectangle", "pentagon", "star"]
        #self.type = np.random.choice(shapes) # inactive for test
        self.type = "pentagon" # active for test
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
        self.make_edge_sequential(self.vertices.copy(), True)
        self.area = self.calculate_area()

    def generate_user_shape(self, vertices):
        self.vertices = vertices.copy()
        self.make_edge_sequential(self.vertices, True)
        self.area = self.calculate_area()

    def draw(self, screen, color = (0, 255, 0)):
        if len(self.vertices) > 2:
            # pygame.draw.polygon(screen, color, self.vertices)
            pygame.draw.polygon(screen, color, self.vertices, width=3) # for test

    def make_edge(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> 'Edge':
        """두 점으로 Edge 생성하고 리스트에 추가한 뒤 추가된 Edge 반환"""
        e1 = Edge(p1, p2)
        self.edges.append(e1)
        return e1

    def make_edge_sequential(self, p_lst: Tuple[Tuple[float, float], ...] | List[Tuple[float, float]], closed: bool = False) -> List['Edge'] | None:
        """순차적으로 연결된 점들로 2개쌍 선택, Edge 생성하고 리스트 추가, 추가된 Edge 리스트 반환
        closed == True이면 첫번째 점으로 돌아가는 Edge도 생성"""
        p_lst = p_lst.copy()
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
        if (closed and (p != self.vertices[0])):
            edge_lst.append(Edge(p, self.vertices[0])) # closed circuit
        self.edges.extend(edge_lst[1:])
        return edge_lst[1:]
        
    def get_intersections(self, new_edge: Edge|None = None) -> Tuple[List[Tuple[float, float]], List['Edge']] | None:
        """현재 Edge 리스트에서 교차하는 Edge들을 검사하고 그 교점 및 교차 Edge들의 리스트를 반환
        새 Edge 추가 여부 선택 가능"""
        if (len(self.edges) == 0):
            return None
        temp_edge_lst = self.edges.copy()
        if (new_edge is not None):
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
    
    def calculate_area(self):
        if (len(self.vertices) < 3):
            return 0
        xy = np.array(self.vertices)/10
        xy -= np.array([40, 30])
        sum = 0
        for i in range(len(xy)):
            sum += xy[i][0]*xy[(i+1)%len(xy)][1] - xy[i][1]*xy[(i+1)%len(xy)][0]
        return abs(sum)/2


    def sutherland_hodgman_clip(self, clip_polygon: 'Shape') -> 'Shape':
        """
        Sutherland Hodgman 다각형 클리핑 알고리즘
        self: 클리핑 대상 다각형
        clip_polygon: 클리핑 다각형 (볼록 다각형 가정)
        반환값: 클리핑 후 남는 다각형
        """
        output_list = sutherland_hodgman_clip(self.get_vertices(), clip_polygon.get_vertices())
        new_shape = Shape(self.screen)
        if len(output_list) > 0:
            new_shape.generate_user_shape(output_list)
        new_shape.draw(self.screen, (255,0,0)) # for test
        return new_shape
