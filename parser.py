import os
import pandas as pd
import json

path = "/home/crescom01/문서/BA_label_point"
label_list = ['top','middle','thumb']
data_list = { "file_name": [], "top_x": [], "top_y": [], "middle_x": [], "middle_y": [], "thumb_x": [],
                 "thumb_y": []}
file_list = [file for file in os.listdir(path) if file.endswith(".json")]
for _ in file_list:
    data_list['file_name'].append(_)
    with open(str(path+'/'+_)) as json_file:
        json_file = json.load(json_file)

        for index, json_dict in enumerate(json_file['shapes']):
             data_list[str(label_list[index]+'_x')].append(json_dict['points'][0][0])
             data_list[str(label_list[index]+'_y')].append(json_dict['points'][0][1])

result_data = pd.DataFrame(data_list)
print(result_data)
result_data.to_excel(excel_writer='key_point.xlsx')

