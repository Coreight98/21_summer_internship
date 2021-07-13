import cv2

#3 keypoints 좌표 필요
def position_checker(image_path,top,middle,thumb):
    img = cv2.imread(image_path)
    image_height,image_width = img.shape[0],img.shape[1]

    #3 keypoints 좌표가 있는지, 확인
    if not (top and middle and thumb):
        #에러
        return 0
    #top과 middle 사이의 기울기
    dt = (top[0] - middle[0])/(top[1] - middle[1])

    if middle[0] > thumb[0]:
        #좌우 반전
        # 조건1: 180도 회전
        if top[1] - middle[1] <0:
            img = cv2.rotate(img, cv2.ROTATE_180)
            top[0],top[1] = image_width - top[0],image_height-top[1]
            middle[0],middle[1] = image_width - middle[0],image_height - middle[1]
            thumb[0],thumb[1] = image_width - thumb[0],image_height - thumb[1]
        # 좌우 반전
        else:
            img = cv2.flip(img, 1)
            top[0] = image_width - top[0]
            middle[0] = image_width - middle[0]
            thumb[0] = image_width - thumb[0]
    elif top[1] - middle[1] <0:
        #상하반전
        img = cv2.flip(img, 0)
        top[1] = image_height - top[1]
        middle[1] = image_height - middle[1]
        thumb[1] = image_height - thumb[1]
    elif -1<= top[0] - middle[0] <= 1:
        #방향 조정
        #조건1: 90도 회전
        if top[1] >= thumb[1]:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            top[0], top[1] = top[1],image_height -  top[0]
            middle[0], middle[1] = middle[1], image_height - middle[0]
            thumb[0], thumb[1] = thumb[1], image_height - thumb[0]
        #조건2: 270도 회전
        else:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            top[0], top[1] = image_width - top[1], top[0]
            middle[0], middle[1] = image_width - middle[1], middle[0]
            thumb[0], thumb[1] = image_width - thumb[1], thumb[0]
    # 양손 검출 조건
    else:
        #정상적인 왼손
        pass
    return [img,[top,middle,thumb]]