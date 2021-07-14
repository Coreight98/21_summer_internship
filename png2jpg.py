path = '/home/crescom01/문서/BA_test_pic/'
from PIL import Image
import os

file_list = [file for file in os.listdir(path) if file.endswith('.png')]

for file in file_list:
    try:
        # open image in png format
        img_png = Image.open(str(path+file))
        img_png = img_png.convert("RGB")
        # The image object is used to save the image in jpg format
        img_png.save('/home/crescom01/문서/temp/'+file.split('.png')[0]+'.jpg')
    except:
        print(file)