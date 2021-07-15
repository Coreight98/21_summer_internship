import cv2
import matplotlib.pyplot as plt
import math
import imutils
import numpy as np
import json
import os
    # 3 keypoints 좌표 필요
def rotation(image, angleInDegrees):
    h, w = image.shape[:2]
    img_c = (w / 2, h / 2)
    rot = cv2.getRotationMatrix2D(img_c, angleInDegrees, 1)
    rad = math.radians(angleInDegrees)
    sin = math.sin(rad)
    cos = math.cos(rad)
    b_w = int((h * abs(sin)) + (w * abs(cos)))
    b_h = int((h * abs(cos)) + (w * abs(sin)))
    rot[0, 2] += ((b_w / 2) - img_c[0])
    rot[1, 2] += ((b_h / 2) - img_c[1])
    outImg = cv2.warpAffine(image, rot, (b_w, b_h), flags=cv2.INTER_LINEAR)
    return outImg
def position_checker(image_path,top,middle,thumb):
    img = cv2.imread(image_path)
    try:
        angle = math.atan2(top[0]-middle[0],middle[1]-top[1])
        angle = math.degrees(angle)
        print(angle)
        #시계방향 90도
        if 45<= angle<=135:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_height, image_width = img.shape[0], img.shape[1]
            top[0], top[1] = top[1],image_height -  top[0]
            middle[0], middle[1] = middle[1], image_height - middle[0]
            thumb[0], thumb[1] = thumb[1], image_height - thumb[0]
        #반시계방향 90도
        elif -135<= angle<=-45:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            image_height, image_width = img.shape[0], img.shape[1]
            top[0], top[1] = image_width - top[1], top[0]
            middle[0], middle[1] = image_width - middle[1], middle[0]
            thumb[0], thumb[1] = image_width - thumb[1], thumb[0]
        #180도
        elif 135<= angle<=225 or -225<=angle<=-135:
            img = cv2.rotate(img, cv2.ROTATE_180)
            image_height, image_width = img.shape[0], img.shape[1]
            top[0],top[1] = image_width - top[0],image_height-top[1]
            middle[0],middle[1] = image_width - middle[0],image_height - middle[1]
            thumb[0],thumb[1] = image_width - thumb[0],image_height - thumb[1]
        #좌우 대칭
        if middle[0] > thumb[0]:
            img = cv2.flip(img, 1)
            image_height, image_width = img.shape[0], img.shape[1]
            top[0] = image_width - top[0]
            middle[0] = image_width - middle[0]
            thumb[0] = image_width - thumb[0]
        #양손 사진일 경우 왼손만 인식하기 위해 사진크기 조정
        image_height, image_width = img.shape[0], img.shape[1]
        if middle[0] < image_width//2 and top[0]< image_width//2 and thumb[0]< image_width//2:
            flip_thumb_x = image_width - thumb[0]
            cutting_x_position = thumb[0]+flip_thumb_x/5
            img = img[0:image_height, 0: int(cutting_x_position)]
        #좌표에 점 찍기
        img = cv2.circle(img, (int(top[0]),int(top[1])), 6, (0, 0, 255), -1)
        img = cv2.circle(img, (int(middle[0]),int(middle[1])), 6, (0, 0, 255), -1)
        img = cv2.circle(img, (int(thumb[0]),int(thumb[1])), 6, (0, 0, 255), -1)
        angle = math.atan2(top[0] - middle[0], middle[1] - top[1])
        angle = math.degrees(angle)
        if -60<=angle<=60:
            img = rotation(img,angle)
        # plt.imshow(img)
        # plt.show()

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

        # 반환 값 이미지, 3 keypoints의 좌표값
        return [img, [top, middle, thumb]]
    except:
        return [img]


image_path = '/home/crescom01/PycharmProjects/handbone_key_point/BA_label_point/image/'
json_path = '/home/crescom01/PycharmProjects/handbone_key_point/BA_label_point/json/'
test_output_path = '/home/crescom01/PycharmProjects/handbone_key_point/test_output'
file_list = [file for file in os.listdir(image_path) if file.endswith('.jpg')]
#file_list = ['1455.jpg','1469.jpg']
#file_list = ['kh_219.jpg']
for f in file_list:
    image_name = f.split('.jpg')[0]
    with open(str(json_path + '/' + image_name + '.json')) as json_file:
        json_file = json.load(json_file)
        for j in json_file['shapes']:
            if j['label'] == 'top':
                top = [j['points'][0][0], j['points'][0][1]]
            elif j['label'] == 'middle':
                middle = [j['points'][0][0], j['points'][0][1]]
            elif j['label'] == 'thumb':
                thumb = [j['points'][0][0], j['points'][0][1]]
        result = position_checker(str(image_path + image_name + '.jpg'), top, middle, thumb)[0]
        if result != []:
            cv2.imwrite(str(test_output_path + '/' + f), result)
#position_checker('/home/crescom01/PycharmProjects/handbone_key_point/BA_test_pic/image/4419.jpg',[1511.6883116883116,580.5194805194805],[1414.2857142857142,1842.857142857143],[1896.103896103896,1768.8311688311687])
#position_checker('/home/crescom01/PycharmProjects/handbone_key_point/BA_label_point/image/1377_reform.jpg',[1938.8453608247423,758.020618556701],[624.1904761904761,783.7142857142858],[760.0816326530612,1224.6326530612246])