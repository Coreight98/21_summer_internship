path = '/home/crescom01/PycharmProjects/handbone_key_point/BA_label_point/json/val/'
image_path = '/home/crescom01/PycharmProjects/handbone_key_point/BA_label_point/image/val/'
save_path = '/home/crescom01/PycharmProjects/handbone_key_point/temp_png/'
import os
import json
import cv2
import base64
from io import BytesIO
file_list = [file for file in os.listdir(path) if file.endswith('.json')]
for _ in file_list:
    temp = _.split('.json')[0]
    with open(str(path+'/'+_)) as json_file:
        json_file = json.load(json_file)
        image = cv2.imread(str(image_path + temp+'.jpg'))
        retval, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer)
        json_file["imagePath"] = str(temp+'.jpg')
        json_file["imageData"] = jpg_as_text.decode('utf8')
        json_file["imageHeight"] = image.shape[0]
        json_file["imageWidth"] = image.shape[1]
        with open(str(save_path + temp + ".json"), 'w') as json_re:
            json.dump(json_file, json_re, indent="")