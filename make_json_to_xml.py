import json, os, math, shutil, cv2, csv
import matplotlib.pyplot as plt
point_list = ['top','middle','thumb'] # fm tl tm
img_path = '/home/crescom01/PycharmProjects/handbone_key_point/BA_label_point/image' + '/'
train_save_path = 'deep-high-resolution-net.pytorch/data/handbone/images/train' + '/'
val_save_path = 'deep-high-resolution-net.pytorch/data/handbone/images/val' + '/'
xml_path = '/home/crescom01/PycharmProjects/handbone_key_point/json_new' + '/'
#val_xml_path = '/home/crescom01/PycharmProjects/handbone_key_point/json_new/val' + '/'
save_path = 'deep-high-resolution-net.pytorch/data/handbone/annotations' + '/'
# point_list = ['c1e','c2e','c3e','c4e','c5e','c6e','c1c','c2c','c3c','c4c','c5c','c6c']
# img_path = '/media/crescom/새 볼륨1/dataset/spine/train_c/c_img' + '/'
# train_save_path = '/home/crescom/PycharmProjects/deep-high-resolution-net.pytorch-master/data/new_c_spine/images/train' + '/'
# val_save_path = '/home/crescom/PycharmProjects/deep-high-resolution-net.pytorch-master/data/new_c_spine/images/val' + '/'
#
# xml_path = '/media/crescom/새 볼륨1/dataset/spine/train_c/c_xml' + '/'
# save_path = '/home/crescom/PycharmProjects/deep-high-resolution-net.pytorch-master/data/new_c_spine/annotations' + '/'
xml_list = sorted(os.listdir(xml_path))


def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

makedir(train_save_path)
makedir(val_save_path)
makedir(save_path)

def coco_keypoint():
    csv_write_info = [['original file name', 'change file name']]

    train_y_dict = {'images':[],'annotations':[],'categories':[]}
    val_y_dict = {'images':[],'annotations':[],'categories':[]}

    split_cnt = math.ceil(len(xml_list) * 0.9)
    train_xml_list = xml_list[:split_cnt]
    val_xml_list = xml_list[split_cnt:]


    id_cnt = 0
    ann_id = 1000000

    ####################################### train json save
    train_y_dict['categories'].append({'supercategory': 'handbone', 'id': 1, 'name': 'handbone',
                                       'keypoints': point_list,
                                       'skeleton': [[0, 1], [1, 2]]})
    # 'skeleton': [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12]]})


    for one_xml in train_xml_list:
        xml_dict = {}
        with open(xml_path + one_xml,'r') as file:
            lines = file.readlines()
            for one_line in lines:
                # print(one_line)
                if '<name>' in one_line:
                    class_name = one_line.replace('name','').replace('/','').replace('<','').replace('>','').replace(' ','').replace('\t','').replace('\n','')
                    xml_dict[class_name] = []
                elif 'xmin' in one_line:
                    xmin = one_line.replace('xmin', '').replace('/', '').replace('<', '').replace('>', '').replace(' ','').replace('\t','').replace('\n','')
                    xml_dict[class_name].append(int(float(xmin)))
                elif 'ymin' in one_line:
                    ymin = one_line.replace('ymin', '').replace('/', '').replace('<', '').replace('>', '').replace(' ','').replace('\t','').replace('\n','')
                    xml_dict[class_name].append(int(float(ymin)))

        img_name = one_xml.replace('.xml','.jpg')
        img = cv2.imread(img_path + img_name)
        img_y, img_x = img.shape[0], img.shape[1]

        id_cnt += 1
        ann_id += 1
        train_y_dict['images'].append({'file_name':str(id_cnt) + '.jpg', 'id': id_cnt, 'height':img_y, 'width':img_x})
        num_keypoint = 0

        csv_write_info.append([img_name, str(id_cnt) + '.jpg'])

        temp_xml_list = []
        temp_x = []
        temp_y = []

        for one_point_name in point_list:
            # if one_point_name == 'c2e':
            #     box_xmin = xml_dict[one_point_name][0]
            #     box_ymin = xml_dict[one_point_name][1]
            # if one_point_name == 'c6c':
            #     box_xmax = xml_dict[one_point_name][0]
            #     box_ymax = xml_dict[one_point_name][1]

            if one_point_name in xml_dict.keys():
                # temp_xml_list.append([xml_dict[one_point_name][0], xml_dict[one_point_name][1]])
                temp_xml_list.append(xml_dict[one_point_name][0])
                temp_xml_list.append(xml_dict[one_point_name][1])
                temp_xml_list.append(2)
                num_keypoint += 1

                temp_x.append(xml_dict[one_point_name][0])
                temp_y.append(xml_dict[one_point_name][1])
            else:
                # temp_xml_list.append([0, 0])
                temp_xml_list.append(0)
                temp_xml_list.append(0)
                temp_xml_list.append(0)

        box_xmin, box_xmax = min(temp_x), max(temp_x)
        box_ymin, box_ymax = min(temp_y), max(temp_y)
        img_x = abs(box_xmax - box_xmin)
        img_y = abs(box_ymax - box_ymin)

        # bbox 기준을 point xmin / xmax / ymin / ymax 기준에서 + 30% 만큼의 넓이로 설정
        x = 0 if box_xmin - int(img_x * 0.2) < 0 else box_xmin - int(img_x * 0.2)
        y = 0 if box_ymin - int(img_y * 0.2) < 0 else box_ymin - int(img_y * 0.2)
        w = (box_xmax + int(img_x * 0.2)) - x
        h = (box_ymax + int(img_y * 0.2)) - y

        # print(temp_xml_list)
        train_y_dict['annotations'].append({'num_keypoints':num_keypoint, 'keypoints': temp_xml_list,
                                            'image_id':id_cnt, 'category_id':1,
                                            'bbox':[0,0,img.shape[0], img.shape[1]],
                                            'area':img.shape[0]*img.shape[1], 'iscrowd':0,
                                            'id':ann_id})

        #### if xml file exist, you bring image file having same xml file name
        one_img_name = one_xml.replace('.xml', '.jpg')
        one_img_path = img_path + one_img_name
        shutil.copy(one_img_path, train_save_path + '%012d.jpg' % id_cnt)


    ####################################### validation json save
    val_y_dict['categories'].append({'supercategory': 'handbone', 'id': 1, 'name': 'handbone',
                                     'keypoints': point_list,
                                     'skeleton': [[0, 1], [1, 2]]})
    # 'skeleton': [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12]]})


    for one_xml in val_xml_list:
        xml_dict = {}
        with open(xml_path + one_xml, 'r') as file:
            lines = file.readlines()
            for one_line in lines:
                # print(one_line)
                if '<name>' in one_line:
                    class_name = one_line.replace('name', '').replace('/', '').replace('<', '').replace('>',
                                                                                                        '').replace(' ',
                                                                                                                    '').replace(
                        '\t', '').replace('\n', '')
                    xml_dict[class_name] = []
                elif 'xmin' in one_line:
                    xmin = one_line.replace('xmin', '').replace('/', '').replace('<', '').replace('>', '').replace(' ',
                                                                                                                   '').replace(
                        '\t', '').replace('\n', '')
                    xml_dict[class_name].append(int(float(xmin)))
                elif 'ymin' in one_line:
                    ymin = one_line.replace('ymin', '').replace('/', '').replace('<', '').replace('>', '').replace(' ',
                                                                                                                   '').replace(
                        '\t', '').replace('\n', '')
                    xml_dict[class_name].append(int(float(ymin)))

        img_name = one_xml.replace('.xml', '.jpg')
        img = cv2.imread(img_path + img_name)
        img_y, img_x = img.shape[0], img.shape[1]

        id_cnt += 1
        ann_id += 1
        val_y_dict['images'].append({'file_name': str(id_cnt) + '.jpg', 'id': id_cnt, 'height': img_y, 'width': img_x})
        num_keypoint = 0

        csv_write_info.append([img_name, str(id_cnt) + '.jpg'])

        temp_xml_list = []
        temp_x = []
        temp_y = []

        for one_point_name in point_list:
            # if one_point_name == 'c2e':
            #     box_xmin = xml_dict[one_point_name][0]
            #     box_ymin = xml_dict[one_point_name][1]
            # elif one_point_name == 'c6c':
            #     box_xmax = xml_dict[one_point_name][0]
            #     box_ymax = xml_dict[one_point_name][1]

            if one_point_name in xml_dict.keys():
                # temp_xml_list.append([xml_dict[one_point_name][0], xml_dict[one_point_name][1]])
                temp_xml_list.append(xml_dict[one_point_name][0])
                temp_xml_list.append(xml_dict[one_point_name][1])
                temp_xml_list.append(2)
                num_keypoint += 1

                temp_x.append(xml_dict[one_point_name][0])
                temp_y.append(xml_dict[one_point_name][1])
            else:
                # temp_xml_list.append([0, 0])
                temp_xml_list.append(0)
                temp_xml_list.append(0)
                temp_xml_list.append(0)

        # x = 0 if box_xmin - int(img_x*0.1) < 0 else box_xmin - int(img_x*0.1)
        # y = 0 if box_ymin - int(img_y*0.1) < 0 else box_ymin - int(img_y*0.1)
        # w = (box_xmax + int(img_x*0.15)) - x
        # h = (box_ymax + int(img_y*0.15)) - y

        box_xmin, box_xmax = min(temp_x), max(temp_x)
        box_ymin, box_ymax = min(temp_y), max(temp_y)
        img_x = abs(box_xmax - box_xmin)
        img_y = abs(box_ymax - box_ymin)

        # bbox 기준을 point xmin / xmax / ymin / ymax 기준에서 + 30% 만큼의 넓이로 설정
        x = 0 if box_xmin - int(img_x * 0.2) < 0 else box_xmin - int(img_x * 0.2)
        y = 0 if box_ymin - int(img_y * 0.2) < 0 else box_ymin - int(img_y * 0.2)
        w = (box_xmax + int(img_x * 0.2)) - x
        h = (box_ymax + int(img_y * 0.2)) - y


        # print(temp_xml_list)
        val_y_dict['annotations'].append({'num_keypoints': num_keypoint, 'keypoints': temp_xml_list,
                                            'image_id': id_cnt, 'category_id': 1,
                                            'bbox': [0,0, img.shape[0], img.shape[1]],
                                            'area': img.shape[0] * img.shape[1], 'iscrowd': 0,
                                            'id': ann_id})

        #### if xml file exist, you bring image file having same xml file name
        one_img_name = one_xml.replace('.xml', '.jpg')
        one_img_path = img_path + one_img_name
        shutil.copy(one_img_path, val_save_path + '%012d.jpg' % id_cnt)

        # img = img[y:y + h, x:x + w, :]
        # plt.imshow(img)
        # plt.show()

    print(train_y_dict['images'][0:4])
    print(train_y_dict['annotations'][0:4])
    #
    # json_data = json.dumps(train_y_dict,indent=4)
    # print(json_data)

    with open(save_path + 'handbone_train.json','w') as train_json_file:
        json.dump(train_y_dict, train_json_file)
    with open(save_path + 'handbone_val.json','w') as val_json_file:
        json.dump(val_y_dict, val_json_file)
    with open(save_path + 'file_name.csv','w', encoding='utf-8',newline='') as f:
        wr = csv.writer(f)
        for line in csv_write_info:
            wr.writerow(line)


def mpii_keypoint():
    train_y_dict = []
    val_y_dict = []

    split_cnt = math.ceil(len(xml_list) * 0.8)
    train_xml_list = xml_list[:split_cnt]
    val_xml_list = xml_list[split_cnt:]


    for one_xml in train_xml_list:
        with open(xml_path + one_xml, 'r') as file:
            lines = file.readlines()
            for one_line in lines:
                # print(one_line)
                if '<name>' in one_line:
                    class_name = one_line.replace('name', '').replace('/', '').replace('<', '').replace('>',
                                                                                                        '').replace(' ',
                                                                                                                    '').replace(
                        '\t', '').replace('\n', '')
                    xml_dict[class_name] = []
                elif 'xmin' in one_line:
                    xmin = one_line.replace('xmin', '').replace('/', '').replace('<', '').replace('>', '').replace(' ',
                                                                                                                   '').replace(
                        '\t', '').replace('\n', '')
                    xml_dict[class_name].append(int(xmin))
                elif 'ymin' in one_line:
                    ymin = one_line.replace('ymin', '').replace('/', '').replace('<', '').replace('>', '').replace(' ',
                                                                                                                   '').replace(
                        '\t', '').replace('\n', '')
                    xml_dict[class_name].append(int(ymin))

            temp_xml_list = []
            temp_joint_vis = []

            for one_point_name in point_list:
                try:
                    temp_joint_vis.append(1)
                    temp_xml_list.append([float(xml_dict[one_point_name][0]), float(xml_dict[one_point_name][1])])
                    # temp_xml_list.append(xml_dict[one_point_name][0])
                    # temp_xml_list.append(xml_dict[one_point_name][1])
                except:
                    temp_joint_vis.append(0)
                    temp_xml_list.append([-1.0, -1.0])
                    # temp_xml_list.append(0)
                    # temp_xml_list.append(0)

            # print(temp_xml_list)
            train_y_dict.append({'joints_vis': temp_joint_vis, 'joints': temp_xml_list, 'image': one_xml.replace('.xml', '.jpg')})

    print(train_y_dict)

# mpii_keypoint()
coco_keypoint()