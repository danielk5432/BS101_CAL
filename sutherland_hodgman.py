def sutherland_hodgman_clip(subject_polygon, clip_polygon):
    """
    Sutherland–Hodgman polygon clipping algorithm
    subject_polygon : [(x, y), ...]
    clip_polygon : [(x, y), ...]
    """
    
    def inside(p, cp1, cp2):
        # 점 p가 클리핑 에지 cp1->cp2의 왼쪽(내부)에 있는지 확인
        # 벡터의 외적을 이용해 방향 판별
        return (cp2[0] - cp1[0])*(p[1]-cp1[1]) - (cp2[1]-cp1[1])*(p[0]-cp1[0]) >= 0

    def compute_intersection(s, p, cp1, cp2):
        # 선분 s->p 와 cp1->cp2 의 교차점 계산
        # 교차점 파라미터 t 이용: I = S + t(P-S)
        # 두 선분의 방정식을 파라메트릭 형태로 풀어서 t를 구한다.
        
        # Line S-P parameters
        dx = p[0] - s[0]
        dy = p[1] - s[1]

        # Clipper edge parameters
        cx = cp2[0] - cp1[0]
        cy = cp2[1] - cp1[1]

        # Solve the intersection t from line equations
        denom = (cx*dy - cy*dx)
        if denom == 0:
            # 병렬 혹은 교차점 없음
            # 특별히 처리하지 않고 그냥 s 반환(이 경우는 거의 없음)
            return s

        t = ((cp1[0]-s[0])*dy - (cp1[1]-s[1])*dx) / denom
        
        # 교차점
        return (s[0] + t*cx, s[1] + t*cy)

    output_list = subject_polygon[:]
    cp_count = len(clip_polygon)

    for i in range(cp_count):
        cp1 = clip_polygon[i]
        cp2 = clip_polygon[(i+1) % cp_count]

        input_list = output_list
        output_list = []

        if len(input_list) == 0:
            # 이미 잘려서 다각형이 없어진 경우
            break

        s = input_list[-1]

        for p in input_list:
            if inside(p, cp1, cp2):
                if not inside(s, cp1, cp2):
                    # s는 밖, p는 안 -> 교차점 + p
                    intersec = compute_intersection(s, p, cp1, cp2)
                    output_list.append(intersec)
                # p는 안 -> p 추가
                output_list.append(p)
            elif inside(s, cp1, cp2):
                # s는 안, p는 밖 -> 교차점만 추가
                intersec = compute_intersection(s, p, cp1, cp2)
                output_list.append(intersec)
            s = p

    return output_list

# 예제 사용
if __name__ == "__main__":
    # 대상 다각형(예: 사각형)
    subject_polygon = [(50,50), (200,50), (200,200), (50,200)]
    # 클리핑 다각형(예: 삼각형)
    clip_polygon = [(100,100), (300,100), (200,300)]

    clipped = sutherland_hodgman_clip(subject_polygon, clip_polygon)
    print("Clipped polygon:", clipped)
