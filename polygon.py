import pygame
import numpy as np

Width, Height = 800, 600

# 목표 도형의 면적을 계산하는 함수
def area(xy):
    xy = np.array(xy) / 10  
    xy -= np.array([40, 30])  
    sum_area = 0
    for i in range(len(xy)):
        sum_area += xy[i][0] * xy[(i + 1) % len(xy)][1] - xy[i][1] * xy[(i + 1) % len(xy)][0]
    return abs(sum_area) / 2

# 목표 도형의 면적을 계산하는 함수
def calculate_target_area(target_polygon):
    return area(target_polygon)

# 목표 도형의 초기화 함수
def init_goal():
    min_vert, max_vert = 4, 10
    target_vertices = np.random.randint(min_vert, max_vert)  
    target_polygon = generate_target_polygon(target_vertices)  
    target_area = calculate_target_area(target_polygon)  
    return target_vertices, target_area, target_polygon

# 목표 도형을 생성하는 함수 (랜덤한 꼭짓점 위치)
def generate_target_polygon(target_vertices):
    angle = 2 * np.pi / target_vertices
    radius = 100  
    center = (Width // 2, Height // 2)  
    vertices = []
    
    for i in range(target_vertices):
        x = center[0] + radius * np.cos(i * angle)
        y = center[1] + radius * np.sin(i * angle)
        vertices.append((x, y))
    
    return vertices

# 도형이 다른 도형에 포함되는지 확인하는 함수
def is_polygon_contained(inner_polygon, outer_polygon):
    def is_point_in_polygon(point, polygon):
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    for point in inner_polygon:
        if not is_point_in_polygon(point, outer_polygon):
            return False
    return True

def calculate_similarity(player_area, target_area, player_polygon, target_polygon):
    if player_area == 0:  
        return 0
    
    if player_area > target_area:
        return target_area / player_area
    
    if is_polygon_contained(target_polygon, player_polygon):
        contained_area = sum([area([target_polygon[i], target_polygon[(i + 1) % len(target_polygon)], player_polygon[i]]) 
                              for i in range(len(player_polygon))])
        return contained_area / player_area
    
    return min(player_area / target_area, 1.0)

# 목표 도형 정보를 화면에 표시하는 함수
def display_goal(screen, target_vertices, target_area):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(f'Number of Vertices: {target_vertices}', True, (255, 255, 255))
    screen.blit(text, (Width - 350, Height - 100))
    text = font.render(f'Target Area: {target_area}', True, (255, 255, 255))
    screen.blit(text, (Width - 350, Height - 50))

# 도형의 면적을 화면에 표시하는 함수
def display_area(screen, xy):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(f'Area: {area(xy):.1f}', True, (255, 255, 255))
    screen.blit(text, (20, 5))

# 크레딧을 표시하는 함수
def display_credits(screen, credits):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(f'Credits: {credits}', True, (255, 255, 255))
    screen.blit(text, (20, Height - 50))

# Pygame 초기화
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((Width, Height))

play, num_vertices, xy = True, 0, []
target_vertices, target_area, target_polygon = init_goal()  
display_goal(screen, target_vertices, target_area)  
isdrawn = False
credits = 100  
attempts = 0  

# 메인 게임 루프
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.button)  
            if event.button == 2 or isdrawn:  
                isdrawn = False
                screen.fill((0, 0, 0))  
                num_vertices, xy = 0, [] 
                target_vertices, target_area, target_polygon = init_goal()  
                display_goal(screen, target_vertices, target_area)  
                credits -= 10  
                attempts += 1 
            if event.button == 1:  
                num_vertices += 1
                x, y = pygame.mouse.get_pos()
                xy.append((x, y)) 
                pygame.draw.circle(screen, (255, 255, 255), (x, y), 3) 
            if event.button == 3 and num_vertices > 2: 
                pygame.draw.polygon(screen, (255, 255, 255), xy)  
                player_area = area(xy)  
                display_area(screen, xy) 
                similarity = calculate_similarity(player_area, target_area, xy, target_polygon) 
                print(f'Similarity: {similarity:.2f}') 
                isdrawn = True  

    pygame.draw.polygon(screen, (255, 0, 0), target_polygon, 2) 

    display_credits(screen, credits)

    pygame.display.flip() 

pygame.quit() 