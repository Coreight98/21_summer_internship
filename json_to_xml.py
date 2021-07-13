import os, sys
from xml.etree.ElementTree import parse, Element, SubElement, ElementTree, dump
import json

path = '/home/crescom01/PycharmProjects/handbone_key_point/BA_label_point/json/train'
file_list = [file for file in os.listdir(path) if file.endswith(".json")]
for filename in file_list:
    with open(os.path.join(path, filename)) as f:
        json_object = json.load(f)
    # json_object = json.loads(os.path.join(path, filename))
    # print(json_object['imagePath'])
    # print('fl')
    # print(json_object['shapes'][0]['points'][0])
    labelname,xmin,ymin = [],[],[]
    for _ in json_object['shapes']:
        labelname.append('<name>'+_['label']+'</name>')
        xmin.append( '<xmin>' + str(_['points'][0][0]) + '</xmin>')
        # print(xmin)
        ymin.append('<ymin>' + str(_['points'][0][1]) + '</ymin>')
    with open('/home/crescom01/PycharmProjects/handbone_key_point/json_new/train' + '/' +
              json_object['imagePath'].split('.jpg')[0] + '.xml', "w") as file:
        for i in range(len(labelname)):
            file.write(labelname[i] + "\n")
            file.write(xmin[i] + "\n")
            file.write(ymin[i] + "\n")
# assert json_object['id'] == 1
# assert json_object['email'] == 'Sincere@april.biz'
# assert json_object['address']['zipcode'] == '92998-3874'
# assert json_object['admin'] is False
# assert json_object['hobbies'] is None