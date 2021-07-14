import cv2
import matplotlib.pyplot as plt
import math

def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

def ang(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360

    if ang_deg-180>=0:
        # As in if statement
        return 360 - ang_deg
    else:

        return ang_deg

    # 3 keypoints 좌표 필요
def position_checker(image_path,top,middle,thumb):
    main_st = (top[0] - middle[0]) / (top[1] - middle[1])
    sub_st = (thumb[0] - middle[0]) / (thumb[1] - middle[1])
    print(main_st, sub_st)
    img = cv2.imread(image_path)
    plt.imshow(img)
    plt.show()


    # image_height,image_width = img.shape[0],img.shape[1]
    #
    # #3 keypoints 좌표가 있는지, 확인
    # if not (top and middle and thumb):
    #     #에러
    #     return 0
    # #top과 middle 사이의 기울기
    # dt = (top[0] - middle[0])/(top[1] - middle[1])
    #
    # if middle[0] > thumb[0]:
    #     #좌우 반전
    #     # 조건1: 180도 회전
    #     if top[1] - middle[1] <0:
    #         img = cv2.rotate(img, cv2.ROTATE_180)
    #         top[0],top[1] = image_width - top[0],image_height-top[1]
    #         middle[0],middle[1] = image_width - middle[0],image_height - middle[1]
    #         thumb[0],thumb[1] = image_width - thumb[0],image_height - thumb[1]
    #     # 좌우 반전
    #     else:
    #         img = cv2.flip(img, 1)
    #         top[0] = image_width - top[0]
    #         middle[0] = image_width - middle[0]
    #         thumb[0] = image_width - thumb[0]
    # elif top[1] - middle[1] <0:
    #     #상하반전
    #     img = cv2.flip(img, 0)
    #     top[1] = image_height - top[1]
    #     middle[1] = image_height - middle[1]
    #     thumb[1] = image_height - thumb[1]
    # elif -1<= top[0] - middle[0] <= 1:
    #     #방향 조정
    #     #조건1: 90도 회전
    #     if top[1] >= thumb[1]:
    #         img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #         top[0], top[1] = top[1],image_height -  top[0]
    #         middle[0], middle[1] = middle[1], image_height - middle[0]
    #         thumb[0], thumb[1] = thumb[1], image_height - thumb[0]
    #     #조건2: 270도 회전
    #     else:
    #         img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    #         top[0], top[1] = image_width - top[1], top[0]
    #         middle[0], middle[1] = image_width - middle[1], middle[0]
    #         thumb[0], thumb[1] = image_width - thumb[1], thumb[0]
    # # 양손 검출 조건
    # else:
    #     #정상적인 왼손
    #     pass

    #반환 값 이미지, 3 keypoints의 좌표값
    return [img,[top,middle,thumb]]

position_checker('/home/crescom01/PycharmProjects/handbone_key_point/BA_label_point/image/1377_reform.jpg',[1938.8453608247423,758.020618556701],[624.1904761904761,783.7142857142858],[760.0816326530612,1224.6326530612246])