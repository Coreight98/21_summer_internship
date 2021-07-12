import os
import random
import base64
from io import BytesIO
import json
import cv2

# import numpy as np
# from matplotlib import pyplot as plt

path = "/home/crescom01/문서/BA_label_point/"
def augmentation(file_extension):
    file_list = [file for file in os.listdir(path) if file.endswith(file_extension)]
    augmentation_list = ["reverse_R_L","reverse_U_D","rotate_90","rotate_180","rotate_270"]
    for _ in file_list:
        name = _.split(file_extension)[0]
        if "reform" not in name:
            rename = str(name+"_reform")
            image = cv2.imread(str(path+_))
            with open(str(path+name+".json")) as json_file:
                json_file = json.load(json_file)
                choice_pattern = random.choice(augmentation_list)
                if choice_pattern == "reverse_R_L":
                    image = cv2.flip(image,1)
                    for point in json_file["shapes"]:
                        point["points"][0][0] = image.shape[1] - point["points"][0][0]
                elif choice_pattern == "reverse_U_D":
                    image = cv2.flip(image,0)
                    for point in json_file["shapes"]:
                        point["points"][0][1] = image.shape[0] - point["points"][0][1]
                elif choice_pattern == "rotate_90":
                    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                    for point in json_file["shapes"]:
                        temp_x,temp_y = point["points"][0][1],point["points"][0][0]
                        point["points"][0][0] = image.shape[1] - temp_x
                        point["points"][0][1] = temp_y
                elif choice_pattern == "rotate_180":
                    image = cv2.rotate(image, cv2.ROTATE_180)
                    for point in json_file["shapes"]:
                        temp_x,temp_y = point["points"][0][1],point["points"][0][0]
                        point["points"][0][0] = image.shape[0] - temp_x
                        point["points"][0][1] = image.shape[1] - temp_y
                elif choice_pattern == "rotate_270":
                    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    for point in json_file["shapes"]:
                        temp_x,temp_y = point["points"][0][1],point["points"][0][0]
                        point["points"][0][0] = temp_x
                        point["points"][0][1] = image.shape[0] - temp_y
                retval, buffer = cv2.imencode(file_extension, image)
                jpg_as_text = base64.b64encode(buffer)
                json_file["imagePath"] = str(rename+file_extension)
                json_file["imageData"] = jpg_as_text.decode('utf8')
                #test
                # jpg_original = base64.b64decode(jpg_as_text)
                # jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
                # img = cv2.imdecode(jpg_as_np, flags=1)
                # plt.imshow(img)
                # plt.show()
                json_file["imageHeight"] = image.shape[0]
                json_file["imageWidth"] = image.shape[1]
                with open(str(path + rename + ".json"),'w') as json_re:
                    json.dump(json_file,json_re, indent="")
            cv2.imwrite(str(path+rename+file_extension),image)
            print(rename+file_extension)

augmentation(".png")
augmentation(".jpg")