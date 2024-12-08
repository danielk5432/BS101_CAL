def sutherland_hodgman(subject_polygon, clip_polygon):
    """
    Sutherland-Hodgman 알고리즘을 통해 subject_polygon을 clip_polygon으로 클리핑한 결과를 반환한다.
    
    :param subject_polygon: [(x1, y1), (x2, y2), ...] 형태의 피클립 다각형 점 리스트
    :param clip_polygon: [(cx1, cy1), (cx2, cy2), ...] 형태의 클리핑 다각형 점 리스트 (볼록 다각형)
    :return: 클리핑된 다각형의 점 리스트
    """
    
    def inside(p, cp1, cp2):
        # 점 p가 클리핑 에지(cp1, cp2)에 대해 내부에 있는지 판별
        # 한 점 p에 대해, 에지 방향(벡터)을 기준으로 왼쪽에 있으면 inside로 간주
        return (cp2[0] - cp1[0])*(p[1] - cp1[1]) - (cp2[1] - cp1[1])*(p[0] - cp1[0]) >= 0

    def intersect(s, p, cp1, cp2):
        # 두 선분 (s, p)와 (cp1, cp2)의 교점을 구한다.
        dc = (cp1[0] - cp2[0], cp1[1] - cp2[1])
        dp = (s[0] - p[0], s[1] - p[1])
        n = cp1[0]*cp2[1] - cp1[1]*cp2[0]
        m = s[0]*p[1] - s[1]*p[0]
        denom = dc[0]*dp[1] - dc[1]*dp[0]
        if denom == 0:
            # 거의 평행하거나 교점이 없는 경우
            return None
        x = (n*dp[0] - m*dc[0])/denom
        y = (n*dp[1] - m*dc[1])/denom
        return (x, y)
    
    output_list = subject_polygon[:]
    cp_count = len(clip_polygon)
    for i in range(cp_count):
        input_list = output_list
        output_list = []
        
        cp1 = clip_polygon[i]
        cp2 = clip_polygon[(i+1) % cp_count]
        
        if not input_list:
            # 더 이상 클립할 점이 없다면 중단
            break
        
        s = input_list[-1]
        
        for p in input_list:
            if inside(p, cp1, cp2):
                if not inside(s, cp1, cp2):
                    # s는 밖, p는 안 -> 교점 추가 후 p 추가
                    inter = intersect(s, p, cp1, cp2)
                    if inter:
                        output_list.append(inter)
                output_list.append(p)
            elif inside(s, cp1, cp2):
                # s는 안, p는 밖 -> 교점만 추가
                inter = intersect(s, p, cp1, cp2)
                if inter:
                    output_list.append(inter)
            s = p
    
    return output_list


# 예제 사용:
if __name__ == "__main__":
    # 피클립 다각형(주어진 다각형)
    subject = [(50,150), (200,50), (350,150), (350,300), (250,300), (200,250), (150,350), (100,250), (100,200)]
    # 클리핑 다각형(사각형으로 가정)
    clip = [(100,100), (300,100), (300,300), (100,300)]
    
    clipped = sutherland_hodgman(subject, clip)
    print("Clipped Polygon Points:", clipped)
