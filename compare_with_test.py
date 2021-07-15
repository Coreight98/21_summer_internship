import csv
import json
import os
import cv2
test_result_csv_path = '/home/crescom01/PycharmProjects/handbone_key_point/output_bbox/c_handbone_fix_total_add_prob_by_bbox.csv'
#test_result_csv_path = '/home/crescom01/PycharmProjects/handbone_key_point/deep-high-resolution-net.pytorch/data/handbone/test_save/c_handbone_fix_total_add_prob.csv'
test_image_path='/home/crescom01/PycharmProjects/handbone_key_point/BA_test_pic/image'
test_json_path='/home/crescom01/PycharmProjects/handbone_key_point/BA_test_pic/json'
save_abnormal_path = '/home/crescom01/PycharmProjects/handbone_key_point/abnormal_bbox'
def check_over_boundary(boundary_size):
    dict_from_csv = {}
    result_over = []
    to_save_abnormal_data = []
    with open(test_result_csv_path, mode='r') as infile:
        reader = csv.reader(infile)
        for index, rows in enumerate(reader):
            if index == 0:
                for i in rows:
                    dict_from_csv[i] = []
            else:
                for i, j in enumerate(dict_from_csv.keys()):
                    dict_from_csv[j].append(rows[i])
    for image_index, image_name in enumerate(dict_from_csv['file_name']):
        with open(str(test_json_path + '/' + image_name + '.json')) as json_file:
            json_file = json.load(json_file)
            weaky_case_boundary_value = ((json_file['shapes'][0]['points'][0][0] - json_file['shapes'][1]['points'][0][
                0]) ** 2 + (json_file['shapes'][0]['points'][0][1] - json_file['shapes'][1]['points'][0][
                1]) ** 2) ** 0.5 // boundary_size
            temp_result = [image_name,[],[]]
            for label_name in json_file['shapes']:
                label = label_name['label']
                point_x, point_y = float(label_name['points'][0][0]), float(label_name['points'][0][1])
                temp_result[2].append([point_x,point_y])
                test_result_x = float(dict_from_csv[str(label + '_x')][image_index])
                test_result_y = float(dict_from_csv[str(label + '_y')][image_index])
                # print(image_name+'.jpg: ',point_x,point_y,"  ",test_result_x,test_result_y)
                real_distance = ((point_x - test_result_x) ** 2 + (
                        point_y - test_result_y) ** 2) ** 0.5
                if real_distance <= weaky_case_boundary_value:
                    pass
                else:
                    temp_result[1].append([label,[test_result_x,test_result_y]])
                    result_over.append([image_name,str("file_name: {}, over: {}, real_distance: {} px, weaky_distance: {} px" .format(image_name, label,real_distance,weaky_case_boundary_value))])
            if temp_result[1]:
                to_save_abnormal_data.append(temp_result)
    print("boundary_size is {}, count of overrange : {}, ratio: {}%".format(boundary_size, len(result_over),len(result_over)/len(dict_from_csv['file_name'])*100))
    if not os.path.exists(save_abnormal_path+'/'+'boudary'+str(boundary_size)):
        os.makedirs(save_abnormal_path+'/'+'boudary'+str(boundary_size))

    for i in result_over:
        print(i[1])

    print()
    for i in to_save_abnormal_data:
        name = i[0]
        image = cv2.imread(str(test_image_path + '/' + i[0] + '.jpg'))
        for j in i[1]:
            abnormal_data_label = j[0]
            image = cv2.circle(image, (int(j[1][0]),int(j[1][1])), 6,(0,0,255),-1)
        for j in i[2]:
            image = cv2.circle(image, (int(j[0]), int(j[1])), 6, (255, 0, 0), -1)
        cv2.imwrite(str(save_abnormal_path+'/'+'boudary'+str(boundary_size)+'/'+name+'.jpg'), image)




check_over_boundary(10)
check_over_boundary(15)
check_over_boundary(20)
check_over_boundary(30)