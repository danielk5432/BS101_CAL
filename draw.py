import pygame
import numpy as np
from shape import Edge, Shape

class Draw:
    def __init__(self, screen, color=(100, 100, 100), width=3, money=1000, overlap_rate=0.5):
        self.screen = screen
        self.node = []  # 점 리스트
        self.edge = []  # 선 리스트
        self.shape = Shape(screen)  # Shape 객체
        self.color = color  # 도형 색상
        self.width = width  # 선 두께
        self.finished = False  # 도형 완료 여부
        self.money = money  # 초기 돈
        self.overlap_rate = overlap_rate  # 겹치는 면적의 배율

    def node_add(self, x, y):
        """플레이어가 점을 추가할 때 호출"""
        p1 = (x, y)
        if p1 in self.node:
            print("[Error] Node already added!")
            return
        if len(self.node) > 0:  # 기존에 점이 있다면 선을 연결
            p2 = self.node[-1]
            e = Edge(p1, p2)
            if self.check_edge(e):  # 교차되지 않으면 선 추가
                self.edge.append(e)
                pygame.draw.line(self.screen, self.color, p1, p2, self.width)
            else:
                print("[Error] Edge is intersecting!")
                return
        else:
            pygame.draw.circle(self.screen, self.color, p1, self.width)
        
        self.node.append(p1)
        #pygame.draw.circle(self.screen, self.color, p1, self.width)  # 점을 화면에 그림

    def check_edge(self, e1):
        """교차 여부를 확인"""
        for e2 in self.edge[:-1]:  # 마지막 선을 제외하고 확인
            if e1.is_intersecting(e2):
                return False
        return True

    def finish_shape(self):
        """도형을 완성"""
        if len(self.node) < 3:  # 점이 3개 이상이어야 도형이 완성됨
            print("[Error] Shape not finished!")
            return False
        p1 = self.node[0]
        p2 = self.node[-1]
        e1 = Edge(p1, p2)  # 마지막 점과 첫 번째 점 연결
        for e2 in self.edge[1:-1]:  # 첫 번째와 마지막을 제외한 선과 교차 확인
            if e1.is_intersecting(e2):
                print("[Error] Last edge is intersecting!")
                return False
        self.edge.append(e1)  # 마지막 선 추가
        self.shape.generate_user_shape(self.node)  # 도형 생성
        self.shape.draw(self.screen, self.color, fill=True)  # 화면에 도형 그림
        self.finished = True
        return True

    def area(self):
        """도형의 면적 계산"""
        return self.shape.calculate_area()

    def intersect_area(self, shape: 'Shape') -> float:
        """겹치는 면적 계산"""
        self.intersection = self.shape.sutherland_hodgman_clip(shape)  # 겹치는 영역 클리핑
        area = self.intersection.calculate_area()  # 면적 계산
        return area

    """
    def calculate_cost_and_profit(self, target_shape: Shape) -> float:
        그린 도형의 비용 차감 및 수익 계산
        # 그린 도형의 면적만큼 비용 차감
        drawn_area = self.area()
        self.money -= drawn_area  # 면적만큼 돈 차감

        # 목표 도형과 겹치는 면적 계산
        overlap_area = self.intersect_area(target_shape)
        
        # 겹치는 면적에 배율을 곱해 수익 계산
        profit = overlap_area * self.overlap_rate
        self.money += profit  # 수익 추가
        
        print(f"돈: {self.money}, 그린 면적: {drawn_area}, 겹치는 면적: {overlap_area}, 수익: {profit}")
        
            return self.money  # 최종 돈 반환
    """
    def reset(self):
        """도형 리셋"""
        self.node = []
        self.edge = []
        self.finished = False