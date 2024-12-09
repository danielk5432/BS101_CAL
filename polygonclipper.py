import numpy as np
import warnings

# POINTS NEED TO BE PRESENTED CLOCKWISE OR ELSE THIS WONT WORK

class PolygonClipper:
    
    def __init__(self,warn_if_empty=True):
        self.warn_if_empty = warn_if_empty
    
    def is_inside(self, p1, p2, q, epsilon=1e-9):
        R = (p2[0] - p1[0]) * (q[1] - p1[1]) - (p2[1] - p1[1]) * (q[0] - p1[0])
        return R <= epsilon


    def compute_intersection(self, p1, p2, p3, p4, epsilon=1e-9):
        denom = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
        if abs(denom) < epsilon:  # 평행선 체크
            return None
        
        # 두 선분의 교차를 확인
        num1 = (p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])
        num2 = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
        t = num1 / denom
        u = -num2 / denom

        if not (0 <= t <= 1 and 0 <= u <= 1):  # 교차하지 않는 경우
            return None

        # 교차점 계산
        x = p1[0] + t * (p2[0] - p1[0])
        y = p1[1] + t * (p2[1] - p1[1])
        return (x, y)


        
    def clip(self, subject_polygon, clipping_polygon):
        subject_polygon = np.asarray(subject_polygon, dtype=np.float64)
        clipping_polygon = np.asarray(clipping_polygon, dtype=np.float64)
        final_polygon = subject_polygon.copy()

        for i in range(len(clipping_polygon)):
            next_polygon = final_polygon.copy()
            final_polygon = []
            c_edge_start = clipping_polygon[i - 1]
            c_edge_end = clipping_polygon[i]
            print(f"Clipping edge: {c_edge_start} -> {c_edge_end}")

            for j in range(len(next_polygon)):
                s_edge_start = next_polygon[j - 1]
                s_edge_end = next_polygon[j]
                if self.is_inside(c_edge_start, c_edge_end, s_edge_end):
                    if not self.is_inside(c_edge_start, c_edge_end, s_edge_start):
                        intersection = self.compute_intersection(
                            s_edge_start, s_edge_end, c_edge_start, c_edge_end
                        )
                        if intersection:
                            print(f"Adding intersection: {intersection}")
                            final_polygon.append(intersection)
                    final_polygon.append(tuple(s_edge_end))
                elif self.is_inside(c_edge_start, c_edge_end, s_edge_start):
                    intersection = self.compute_intersection(
                        s_edge_start, s_edge_end, c_edge_start, c_edge_end
                    )
                    if intersection:
                        print(f"Adding intersection: {intersection}")
                        final_polygon.append(intersection)
            if len(final_polygon) == 0:
                print("Final polygon is empty. Exiting early.")
                return np.array([])
            print(f"Intermediate polygon: {final_polygon}")
        return np.asarray(final_polygon)


        
    def __call__(self,A,B):
        clipped_polygon = self.clip(A,B)
        if len(clipped_polygon) == 0 and self.warn_if_empty:
            warnings.warn("No intersections found. Are you sure your \
                        polygon coordinates are in clockwise order?")
        
        return clipped_polygon
    
"""
    subject_polygon = [(0,3),(0.5,0.5),(3,0),(0.5,-0.5),(0,-3),(-0.5,-0.5),(-3,0),(-0.5,0.5)]
    clipping_polygon = [(-2,-2),(-2,2),(2,2),(2,-2)]
    
    # star and triangle
    # subject_polygon = [(0,3),(0.5,0.5),(3,0),(0.5,-0.5),(0,-3),(-0.5,-0.5),(-3,0),(-0.5,0.5)]
    # clipping_polygon = [(0,2),(2,-2),(-2,-2)]
    
    subject_polygon = np.array(subject_polygon)
    clipping_polygon = np.array(clipping_polygon)
    clipped_polygon = clip(subject_polygon,clipping_polygon)    
"""

def ensure_clockwise(polygon):
    # Compute signed area
    area = 0
    for i in range(len(polygon)):
        x1, y1 = polygon[i - 1]
        x2, y2 = polygon[i]
        area += (x2 - x1) * (y2 + y1)
    # If area is positive, polygon is counter-clockwise
    if area > 0:
        polygon = polygon[::-1]
    return polygon


def sutherland_hodgman_clip(ss, cc):

    # Ensure polygons are clockwise
    subject_polygon = np.array(ensure_clockwise(ss))
    clipping_polygon = np.array(ensure_clockwise(cc))

    subject_polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]
    clipping_polygon = [(5, 5), (15, 5), (15, 15), (5, 15)]



    print(subject_polygon)
    print(clipping_polygon)

    # Initialize PolygonClipper and perform clipping
    clip_polygon = PolygonClipper()
    clipped_polygon = clip_polygon.clip(subject_polygon, clipping_polygon)

    # Check result
    if len(clipped_polygon) == 0:
        print("No intersection found.")
    else:
        print("Clipped polygon:", clipped_polygon)
    return []