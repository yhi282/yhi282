# 55. car exterior
# path 등 변수는 상황에 맞춰 수정하여 사용하였으니 코드 실행 전 확인 할 것

# 최종 json 생성
import fnmatch
import json
import pandas as pd
import os
import datetime
import shutil
import re
import random


# coco json 불러오기
ins_path = 'C:/Users/MH46/Desktop/cctv55/inspection_json'
file_name_ins = os.listdir(ins_path)
path = []

num = 1
count_num = 1
name_list = pd.DataFrame(columns=['경로', '파일'])



# meta 정보/비교 값 불러오기

for i in file_name_ins:
    path.append(ins_path + '/' + i)

for coco_path in file_name_ins:
    print("______________________________경로 : {}".format(coco_path))
    with open(ins_path + '/' + coco_path, 'r', encoding='UTF-8') as json_file:
        coco_json = json.load(json_file)

    path = 'C:/Users/MH46/Desktop/cctv55_완료/inspection_xlsx'
    file_name = os.listdir(path)
    file_path = []
    for filename in file_name:
            # 현재 task 생성용.
            if coco_path.split('_')[0] + '_' + coco_path.split('_')[1] + '_' + coco_path.split('_')[2] == filename.split('.')[0]:



        # # 예전 task 생성용. task 이름 규칙이 다른 것들은 이걸로
        # for coco_filename in coco_json["images"]:
        #     if coco_filename['file_name'].split('_')[0] + '_' + coco_filename['file_name'].split('_')[2] + '_' + coco_filename['file_name'].split('_')[3] == filename.split('.')[0]:

                file_path = "{}/{}".format(path, filename)
                Ex55 = pd.read_excel(file_path, sheet_name= 0 , header=2, index_col =0)
                Ex55 = Ex55.dropna(axis=0, how='all')


                # datetype 및 표시형식 변환
                ex55_int = 'CCTV 카메라 유형', 'CCTV 설치높이', 'CCTV 각도', '해상도', '촬영방향'
                Ex55['촬영일시\n(yyyy-mm-dd)'] = Ex55['촬영일시\n(yyyy-mm-dd)'].astype(str)
                for Ex55_col in Ex55.columns:
                    if Ex55_col != 'CCTV GPS정보':
                        if Ex55[Ex55_col].dtype == float:
                            Ex55[Ex55_col] = Ex55[Ex55_col].astype(int)
                            if Ex55_col in ex55_int:
                                if Ex55[Ex55_col].dtype != int:
                                        Ex55[Ex55_col] = Ex55[Ex55_col].astype(int)
                            elif Ex55_col not in ex55_int:
                                if Ex55[Ex55_col].dtype != str:
                                    Ex55[Ex55_col] = Ex55[Ex55_col].astype(str)


                # 파일명 정리 - 압축으로 올린것들은 파일명 규칙이 압축폴더 포함해서 들어감
                jpg_name = []
                for i in coco_json['images']:
                    if re.match(".*/.*", str(i['file_name'])):
                        i['file_name'] = i['file_name'].split('/')[1]


                # json 생성
                for i in coco_json['images']:
                    file = i['file_name']
                    match_name = file.split('.')[0]

                    # 전수 검사 json 생성
                    if match_name in new_json:
                        for index, row in Ex55.iterrows():
                            file_split = file.split('_')[0] + '_' + file.split('_')[1] + '_' + file.split('_')[2] + '_' + file.split('_')[3]
                            if file_split == row['원시 파일명']:
                                # 파일명이 존재하는 meta의 경우
                                if row['파일명'] == file.split('.')[0]:

                                    # cr이 아닌 ar/sr은 교차로 유형이 0
                                    if (row['도로 유형'] == 'ar') or (row['도로 유형'] == "sr"):
                                        jpg_name.append(file)
                                        # path 설정
                                        if row['도로 유형'] == 'cr':
                                            path_name = '교차로'
                                        if row['도로 유형'] == 'sr':
                                            path_name = '이면도로'
                                        if row['도로 유형'] == 'ar':
                                            path_name = '접근로'

                                        car_json = {
                                            "Raw Data Info": {
                                                "raw_data_id": file_split,
                                                "location_id": row['촬영장소'],
                                                "location_name": row['촬영장소명'],
                                                "cctv_number": '%02d' % row['촬영방향'],
                                                "copyrighter": "(주)미디어그룹사람과숲",
                                                "resolution": row['해상도'],
                                                "date": row['촬영일시\n(yyyy-mm-dd)'],
                                                "start_time": row['촬영 시작 시간'],
                                                "end_time": row['촬영 종료 시간'],
                                                "length": 3600,
                                                "fps": 30,
                                                "season": row['계절'],
                                                "weather": row['날씨'],
                                                "day_type": row['평일/주말/휴일'],
                                                "road_type": row['도로 유형'],
                                                "cross_type": "",
                                                "cctv_type": row['CCTV 카메라 유형'],
                                                "lens_type": row['CCTV 렌즈 \n유형'],
                                                "cctv_height": row['CCTV 설치높이'],
                                                "cctv_angle": row['CCTV 각도'],
                                                "cctv_gps": row['CCTV GPS정보'],
                                                "file_extension": "mp4"
                                            },
                                            "Source Data Info": {
                                                "source_data_id": row['파일명'],
                                                "classification_id": 'a',
                                                "extract_time": row['추출시간\n(hh:mm:ss)'],
                                                "file_extension": "jpg"},
                                            "Learning Data Info": {
                                                "path": '/차종외관인식/{}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                               '%02d' % row['촬영방향']),
                                                "json_data_id": row['파일명'],
                                                "file_extension": "json",
                                                "annotations": []
                                            }
                                        }

                                        # resolution, gps 데이터타입 및 리스트 확인 수정

                                        if type(car_json["Raw Data Info"]["cctv_gps"]) != list:
                                            if car_json["Raw Data Info"]["cctv_gps"].endswith(']'):
                                                a = car_json["Raw Data Info"]["cctv_gps"][1:-1]
                                                gps1 = a.split(', ')[0]
                                                gps2 = a.split(', ')[1]

                                                car_json["Raw Data Info"]["cctv_gps"] = [gps1, gps2]
                                                car_json["Raw Data Info"]["cctv_gps"] = list(
                                                    map(float, car_json["Raw Data Info"]["cctv_gps"]))
                                            else:
                                                gps1 = car_json["Raw Data Info"]["cctv_gps"].split(', ')[0]
                                                gps2 = car_json["Raw Data Info"]["cctv_gps"].split(', ')[1]

                                                car_json["Raw Data Info"]["cctv_gps"] = [gps1, gps2]
                                                car_json["Raw Data Info"]["cctv_gps"] = list(
                                                    map(float, car_json["Raw Data Info"]["cctv_gps"]))

                                        if type(car_json["Raw Data Info"]["resolution"]) != list:
                                            if car_json["Raw Data Info"]["resolution"].endswith(']'):
                                                a = car_json["Raw Data Info"]["resolution"][1:-1]
                                                gps1 = a.split(', ')[0]
                                                gps2 = a.split(', ')[1]

                                                car_json["Raw Data Info"]["resolution"] = "{}, {}".format(gps1, gps2)
                                        if type(car_json["Raw Data Info"]["resolution"]) == list:
                                            for resolution in car_json["Raw Data Info"]["resolution"]:
                                                if type(resolution) != int:
                                                    car_json["Raw Data Info"]["resolution"] = list(
                                                        map(int, car_json["Raw Data Info"]["resolution"]))

                                        # json bbox 부분 추가
                                        for anno_id in coco_json['annotations']:
                                            for ca_id in coco_json['categories']:
                                                if (anno_id['category_id'] == ca_id['id']) and (anno_id['image_id'] == i['id']):
                                                    if ca_id['name'].split('_')[1] == '버스':
                                                        aaa = {
                                                            "class_id": ca_id['name'].split()[0],
                                                            "type": "bbox",
                                                            "coord": anno_id['bbox'],
                                                            "brand_id": anno_id['attributes']['차량연식선택'],
                                                            "model_id": "Unknown"
                                                        }
                                                        car_json["Learning Data Info"]['annotations'].append(aaa)

                                                        car_json["Raw Data Info"]["start_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["start_time"].split(':')[0]) + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      1] + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      2]
                                                        car_json["Raw Data Info"]["end_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["end_time"].split(':')[0]) + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[
                                                                                                    1] + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[2]

                                                        print("json 생성 완료 : {}".format(car_json))
                                                        print(
                                                            '생성 경로 : {}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                                           row['촬영방향']))

                                                    if ca_id['name'].split('_')[1] != '버스':
                                                        aaa = {
                                                            "class_id": ca_id['name'].split()[0],
                                                            "type": "bbox",
                                                            "coord": anno_id['bbox'],
                                                            "brand_id": ca_id['name'].split('_')[1],
                                                            "model_id": anno_id['attributes']['차량연식선택']
                                                        }
                                                        car_json["Learning Data Info"]['annotations'].append(aaa)

                                                        car_json["Raw Data Info"]["start_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["start_time"].split(':')[0]) + ':' + \
                                                                                                   car_json["Raw Data Info"][
                                                                                                       "start_time"].split(':')[1] + ':' + \
                                                                                                   car_json["Raw Data Info"][
                                                                                                       "start_time"].split(':')[2]
                                                        car_json["Raw Data Info"]["end_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["end_time"].split(':')[0]) + ':' + \
                                                                                                 car_json["Raw Data Info"][
                                                                                                     "end_time"].split(':')[1] + ':' + \
                                                                                                 car_json["Raw Data Info"][
                                                                                                     "end_time"].split(':')[2]

                                                        print("json 생성 완료 : {}".format(car_json))
                                                        print('생성 경로 : {}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                                             row['촬영방향']))


                                                    # 확인 및 저장
                                                    path1 = car_json['Learning Data Info']['path']
                                                    json_path = 'C:/Users/MH46/Desktop/cctv55_완료/55_json/' + file.split('.')[
                                                        0] + '.json'
                                                    with open(json_path, 'w', encoding='UTF-8') as outfile:
                                                        json.dump(car_json, outfile, indent=4, ensure_ascii=False)

                                    # 도로 유형 cr일 경우
                                    if row['도로 유형'] == 'cr':


                                        jpg_name.append(file)

                                        if row['도로 유형'] == 'cr':
                                            path_name = '교차로'
                                        if row['도로 유형'] == 'sr':
                                            path_name = '이면도로'
                                        if row['도로 유형'] == 'ar':
                                            path_name = '접근로'

                                        car_json = {
                                            "Raw Data Info": {
                                                "raw_data_id": file_split,
                                                "location_id": row['촬영장소'],
                                                "location_name": row['촬영장소명'],
                                                "cctv_number": '%02d' % row['촬영방향'],
                                                "copyrighter": "(주)미디어그룹사람과숲",
                                                "resolution": row['해상도'],
                                                "date": row['촬영일시\n(yyyy-mm-dd)'],
                                                "start_time": row['촬영 시작 시간'],
                                                "end_time": row['촬영 종료 시간'],
                                                "length": 3600,
                                                "fps": 30,
                                                "season": row['계절'],
                                                "weather": row['날씨'],
                                                "day_type": row['평일/주말/휴일'],
                                                "road_type": row['도로 유형'],
                                                "cross_type": row['교차로 유형'],
                                                "cctv_type": row['CCTV 카메라 유형'],
                                                "lens_type": row['CCTV 렌즈 \n유형'],
                                                "cctv_height": row['CCTV 설치높이'],
                                                "cctv_angle": row['CCTV 각도'],
                                                "cctv_gps": row['CCTV GPS정보'],
                                                "file_extension": "mp4"
                                            },
                                            "Source Data Info": {
                                                "source_data_id": row['파일명'],
                                                "classification_id": 'a',
                                                "extract_time": row['추출시간\n(hh:mm:ss)'],
                                                "file_extension": "jpg"},
                                            "Learning Data Info": {
                                                "path": '/차종외관인식/{}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                               '%02d' % row['촬영방향']),
                                                "json_data_id": row['파일명'],
                                                "file_extension": "json",
                                                "annotations": []
                                            }
                                        }

                                        # resolution, gps 데이터타입 및 리스트 확인 수정

                                        if type(car_json["Raw Data Info"]["cctv_gps"]) != list:

                                            if car_json["Raw Data Info"]["cctv_gps"].endswith(']'):
                                                a = car_json["Raw Data Info"]["cctv_gps"][1:-1]
                                                gps1 = a.split(', ')[0]
                                                gps2 = a.split(', ')[1]

                                                car_json["Raw Data Info"]["cctv_gps"] = [gps1, gps2]
                                                car_json["Raw Data Info"]["cctv_gps"] = list(
                                                    map(float, car_json["Raw Data Info"]["cctv_gps"]))

                                            else:
                                                gps1 = car_json["Raw Data Info"]["cctv_gps"].split(', ')[0]
                                                gps2 = car_json["Raw Data Info"]["cctv_gps"].split(', ')[1]

                                                car_json["Raw Data Info"]["cctv_gps"] = [gps1, gps2]
                                                car_json["Raw Data Info"]["cctv_gps"] = list(
                                                    map(float, car_json["Raw Data Info"]["cctv_gps"]))

                                        if type(car_json["Raw Data Info"]["resolution"]) != list:
                                            if car_json["Raw Data Info"]["resolution"].endswith(']'):
                                                a = car_json["Raw Data Info"]["resolution"][1:-1]
                                                gps1 = a.split(', ')[0]
                                                gps2 = a.split(', ')[1]

                                                car_json["Raw Data Info"]["resolution"] = "{}, {}".format(gps1, gps2)
                                        if type(car_json["Raw Data Info"]["resolution"]) == list:
                                            for resolution in car_json["Raw Data Info"]["resolution"]:
                                                if type(resolution) != int:
                                                    car_json["Raw Data Info"]["resolution"] = list(
                                                        map(int, car_json["Raw Data Info"]["resolution"]))

                                        # json bbox 부분 추가
                                        for anno_id in coco_json['annotations']:
                                            for ca_id in coco_json['categories']:
                                                if (anno_id['category_id'] == ca_id['id']) and (anno_id['image_id'] == i['id']):

                                                    if ca_id['name'].split('_')[1] == '버스':
                                                        aaa = {
                                                            "class_id": ca_id['name'].split()[0],
                                                            "type": "bbox",
                                                            "coord": anno_id['bbox'],
                                                            "brand_id": anno_id['attributes']['차량연식선택'],
                                                            "model_id": "Unknown"
                                                        }
                                                        car_json["Learning Data Info"]['annotations'].append(aaa)

                                                        car_json["Raw Data Info"]["start_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["start_time"].split(':')[0]) + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      1] + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      2]
                                                        car_json["Raw Data Info"]["end_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["end_time"].split(':')[0]) + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[
                                                                                                    1] + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[2]

                                                        print("json 생성 완료 : {}".format(car_json))
                                                        print(
                                                            '생성 경로 : {}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                                           row['촬영방향']))

                                                    if ca_id['name'].split('_')[1] != '버스':
                                                        aaa = {
                                                            "class_id": ca_id['name'].split()[0],
                                                            "type": "bbox",
                                                            "coord": anno_id['bbox'],
                                                            "brand_id": ca_id['name'].split('_')[1],
                                                            "model_id": anno_id['attributes']['차량연식선택']
                                                        }
                                                        car_json["Learning Data Info"]['annotations'].append(aaa)

                                                        car_json["Raw Data Info"]["start_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["start_time"].split(':')[0]) + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      1] + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      2]
                                                        car_json["Raw Data Info"]["end_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["end_time"].split(':')[0]) + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[
                                                                                                    1] + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[2]

                                                        print("json 생성 완료 : {}".format(car_json))
                                                        print(
                                                            '생성 경로 : {}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                                           row['촬영방향']))

                                                    # 확인 및 저장
                                                    path1 = car_json['Learning Data Info']['path']
                                                    json_path = 'C:/Users/MH46/Desktop/cctv55_완료/55_json/' + file.split('.')[0] + '.json'
                                                    with open(json_path, 'w', encoding='UTF-8') as outfile:
                                                        json.dump(car_json, outfile, indent=4, ensure_ascii=False)

                                # 추출 값이 없는 경우 json 생성
                                if (row['파일명'] == 0) or (row['파일명'] == "0"):
                                    # 도로 유형 ar, sr
                                    if (row['도로 유형'] == 'ar') or (row['도로 유형'] == "sr"):
                                        hh = int(row['촬영 시작 시간'].split(':')[0])
                                        mm = '%02d' % random.randrange(1, 60)
                                        jpg_name.append(file)

                                        if row['도로 유형'] == 'cr':
                                            path_name = '교차로'
                                        if row['도로 유형'] == 'sr':
                                            path_name = '이면도로'
                                        if row['도로 유형'] == 'ar':
                                            path_name = '접근로'

                                        car_json = {
                                            "Raw Data Info": {
                                                "raw_data_id": file_split,
                                                "location_id": row['촬영장소'],
                                                "location_name": row['촬영장소명'],
                                                "cctv_number": '%02d' % row['촬영방향'],
                                                "copyrighter": "(주)미디어그룹사람과숲",
                                                "resolution": row['해상도'],
                                                "date": row['촬영일시\n(yyyy-mm-dd)'],
                                                "start_time": row['촬영 시작 시간'],
                                                "end_time": row['촬영 종료 시간'],
                                                "length": 3600,
                                                "fps": 30,
                                                "season": row['계절'],
                                                "weather": row['날씨'],
                                                "day_type": row['평일/주말/휴일'],
                                                "road_type": row['도로 유형'],
                                                "cross_type": "",
                                                "cctv_type": row['CCTV 카메라 유형'],
                                                "lens_type": row['CCTV 렌즈 \n유형'],
                                                "cctv_height": row['CCTV 설치높이'],
                                                "cctv_angle": row['CCTV 각도'],
                                                "cctv_gps": row['CCTV GPS정보'],
                                                "file_extension": "mp4"
                                            },
                                            "Source Data Info": {
                                                "source_data_id": file.split('.')[0],
                                                "classification_id": 'a',
                                                "extract_time": "{}:{}:{}".format('%02d' % hh, mm, mm),
                                                "file_extension": "jpg"},
                                            "Learning Data Info": {
                                                "path": '/차종외관인식/{}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                               '%02d' % row['촬영방향']),
                                                "json_data_id": file.split('.')[0],
                                                "file_extension": "json",
                                                "annotations": []
                                            }
                                        }

                                        # resolution, gps 데이터타입 및 리스트 확인 수정

                                        if type(car_json["Raw Data Info"]["cctv_gps"]) != list:
                                            if car_json["Raw Data Info"]["cctv_gps"].endswith(']'):
                                                a = car_json["Raw Data Info"]["cctv_gps"][1:-1]
                                                gps1 = a.split(', ')[0]
                                                gps2 = a.split(', ')[1]

                                                car_json["Raw Data Info"]["cctv_gps"] = [gps1, gps2]
                                                car_json["Raw Data Info"]["cctv_gps"] = list(
                                                    map(float, car_json["Raw Data Info"]["cctv_gps"]))
                                            else:
                                                gps1 = car_json["Raw Data Info"]["cctv_gps"].split(', ')[0]
                                                gps2 = car_json["Raw Data Info"]["cctv_gps"].split(', ')[1]

                                                car_json["Raw Data Info"]["cctv_gps"] = [gps1, gps2]
                                                car_json["Raw Data Info"]["cctv_gps"] = list(
                                                    map(float, car_json["Raw Data Info"]["cctv_gps"]))

                                        if type(car_json["Raw Data Info"]["resolution"]) != list:
                                            if car_json["Raw Data Info"]["resolution"].endswith(']'):
                                                a = car_json["Raw Data Info"]["resolution"][1:-1]
                                                gps1 = a.split(', ')[0]
                                                gps2 = a.split(', ')[1]

                                                car_json["Raw Data Info"]["resolution"] = "{}, {}".format(gps1, gps2)
                                        if type(car_json["Raw Data Info"]["resolution"]) == list:
                                            for resolution in car_json["Raw Data Info"]["resolution"]:
                                                if type(resolution) != int:
                                                    car_json["Raw Data Info"]["resolution"] = list(
                                                        map(int, car_json["Raw Data Info"]["resolution"]))

                                        # json bbox 부분 추가
                                        for anno_id in coco_json['annotations']:
                                            for ca_id in coco_json['categories']:
                                                if (anno_id['category_id'] == ca_id['id']) and (anno_id['image_id'] == i['id']):
                                                    if ca_id['name'].split('_')[1] == '버스':
                                                        aaa = {
                                                            "class_id": ca_id['name'].split()[0],
                                                            "type": "bbox",
                                                            "coord": anno_id['bbox'],
                                                            "brand_id": anno_id['attributes']['차량연식선택'],
                                                            "model_id": "Unknown"
                                                        }
                                                        car_json["Learning Data Info"]['annotations'].append(aaa)

                                                        car_json["Raw Data Info"]["start_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["start_time"].split(':')[0]) + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      1] + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      2]
                                                        car_json["Raw Data Info"]["end_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["end_time"].split(':')[0]) + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[
                                                                                                    1] + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[2]

                                                        print("json 생성 완료 : {}".format(car_json))
                                                        print(
                                                            '생성 경로 : {}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                                           row['촬영방향']))

                                                    if ca_id['name'].split('_')[1] != '버스':
                                                        aaa = {
                                                            "class_id": ca_id['name'].split()[0],
                                                            "type": "bbox",
                                                            "coord": anno_id['bbox'],
                                                            "brand_id": ca_id['name'].split('_')[1],
                                                            "model_id": anno_id['attributes']['차량연식선택']
                                                        }
                                                        car_json["Learning Data Info"]['annotations'].append(aaa)

                                                        car_json["Raw Data Info"]["start_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["start_time"].split(':')[0]) + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      1] + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      2]
                                                        car_json["Raw Data Info"]["end_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["end_time"].split(':')[0]) + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[
                                                                                                    1] + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[2]

                                                        print("json 생성 완료 : {}".format(car_json))
                                                        print(
                                                            '생성 경로 : {}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                                           row['촬영방향']))

                                                    # 확인 및 저장
                                                    path1 = car_json['Learning Data Info']['path']
                                                    json_path = 'C:/Users/MH46/Desktop/cctv55_완료/55_json/' + file.split('.')[
                                                        0] + '.json'
                                                    with open(json_path, 'w', encoding='UTF-8') as outfile:
                                                        json.dump(car_json, outfile, indent=4, ensure_ascii=False)

                                    # 도로 유형 cr
                                    if row['도로 유형'] == 'cr':
                                        hh = int(row['촬영 시작 시간'].split(':')[0])
                                        mm = '%02d' % random.randrange(1,60)
                                        jpg_name.append(file)

                                        if row['도로 유형'] == 'cr':
                                            path_name = '교차로'
                                        if row['도로 유형'] == 'sr':
                                            path_name = '이면도로'
                                        if row['도로 유형'] == 'ar':
                                            path_name = '접근로'

                                        car_json = {
                                            "Raw Data Info": {
                                                "raw_data_id": file_split,
                                                "location_id": row['촬영장소'],
                                                "location_name": row['촬영장소명'],
                                                "cctv_number": '%02d' % row['촬영방향'],
                                                "copyrighter": "(주)미디어그룹사람과숲",
                                                "resolution": row['해상도'],
                                                "date": row['촬영일시\n(yyyy-mm-dd)'],
                                                "start_time": row['촬영 시작 시간'],
                                                "end_time": row['촬영 종료 시간'],
                                                "length": 3600,
                                                "fps": 30,
                                                "season": row['계절'],
                                                "weather": row['날씨'],
                                                "day_type": row['평일/주말/휴일'],
                                                "road_type": row['도로 유형'],
                                                "cross_type": row['교차로 유형'],
                                                "cctv_type": row['CCTV 카메라 유형'],
                                                "lens_type": row['CCTV 렌즈 \n유형'],
                                                "cctv_height": row['CCTV 설치높이'],
                                                "cctv_angle": row['CCTV 각도'],
                                                "cctv_gps": row['CCTV GPS정보'],
                                                "file_extension": "mp4"
                                            },
                                            "Source Data Info": {
                                                "source_data_id": file.split('.')[0],
                                                "classification_id": 'a',
                                                "extract_time": "{}:{}:{}".format('%02d' % hh, mm, mm),
                                                "file_extension": "jpg"},
                                            "Learning Data Info": {
                                                "path": '/차종외관인식/{}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'], '%02d' % row['촬영방향']),
                                                "json_data_id": file.split('.')[0],
                                                "file_extension": "json",
                                                "annotations": []
                                                }
                                        }

                                        # resolution, gps 데이터타입 및 리스트 확인 수정

                                        if type(car_json["Raw Data Info"]["cctv_gps"]) != list:
                                            if car_json["Raw Data Info"]["cctv_gps"].endswith(']'):
                                                a = car_json["Raw Data Info"]["cctv_gps"][1:-1]
                                                gps1 = a.split(', ')[0]
                                                gps2 = a.split(', ')[1]

                                                car_json["Raw Data Info"]["cctv_gps"] = [gps1, gps2]
                                                car_json["Raw Data Info"]["cctv_gps"] = list(
                                                    map(float, car_json["Raw Data Info"]["cctv_gps"]))
                                            else:
                                                gps1 = car_json["Raw Data Info"]["cctv_gps"].split(', ')[0]
                                                gps2 = car_json["Raw Data Info"]["cctv_gps"].split(', ')[1]

                                                car_json["Raw Data Info"]["cctv_gps"] = [gps1, gps2]
                                                car_json["Raw Data Info"]["cctv_gps"] = list(
                                                    map(float, car_json["Raw Data Info"]["cctv_gps"]))

                                        if type(car_json["Raw Data Info"]["resolution"]) != list:
                                            if car_json["Raw Data Info"]["resolution"].endswith(']'):
                                                a = car_json["Raw Data Info"]["resolution"][1:-1]
                                                gps1 = a.split(', ')[0]
                                                gps2 = a.split(', ')[1]

                                                car_json["Raw Data Info"]["resolution"] = "{}, {}".format(gps1, gps2)
                                        if type(car_json["Raw Data Info"]["resolution"]) == list:
                                            for resolution in car_json["Raw Data Info"]["resolution"]:
                                                if type(resolution) != int:
                                                    car_json["Raw Data Info"]["resolution"] = list(
                                                        map(int, car_json["Raw Data Info"]["resolution"]))

                                        # json bbox 부분 추가
                                        for anno_id in coco_json['annotations']:
                                            for ca_id in coco_json['categories']:
                                                if (anno_id['category_id'] == ca_id['id']) and (anno_id['image_id'] == i['id']):
                                                    if ca_id['name'].split('_')[1] == '버스':
                                                        aaa = {
                                                            "class_id": ca_id['name'].split()[0],
                                                            "type": "bbox",
                                                            "coord": anno_id['bbox'],
                                                            "brand_id": anno_id['attributes']['차량연식선택'],
                                                            "model_id": "Unknown"
                                                        }
                                                        car_json["Learning Data Info"]['annotations'].append(aaa)

                                                        car_json["Raw Data Info"]["start_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["start_time"].split(':')[0]) + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      1] + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      2]
                                                        car_json["Raw Data Info"]["end_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["end_time"].split(':')[0]) + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[
                                                                                                    1] + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[2]

                                                        print("json 생성 완료 : {}".format(car_json))
                                                        print(
                                                            '생성 경로 : {}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                                           row['촬영방향']))

                                                    if ca_id['name'].split('_')[1] != '버스':
                                                        aaa = {
                                                            "class_id": ca_id['name'].split()[0],
                                                            "type": "bbox",
                                                            "coord": anno_id['bbox'],
                                                            "brand_id": ca_id['name'].split('_')[1],
                                                            "model_id": anno_id['attributes']['차량연식선택']
                                                        }
                                                        car_json["Learning Data Info"]['annotations'].append(aaa)

                                                        car_json["Raw Data Info"]["start_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["start_time"].split(':')[0]) + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      1] + ':' + \
                                                                                                  car_json["Raw Data Info"][
                                                                                                      "start_time"].split(':')[
                                                                                                      2]
                                                        car_json["Raw Data Info"]["end_time"] = '{:0>2s}'.format(
                                                            car_json["Raw Data Info"]["end_time"].split(':')[0]) + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[
                                                                                                    1] + ':' + \
                                                                                                car_json["Raw Data Info"][
                                                                                                    "end_time"].split(':')[2]

                                                        print("json 생성 완료 : {}".format(car_json))
                                                        print(
                                                            '생성 경로 : {}/[{}]{}/{}번'.format(path_name, row['촬영장소'], row['촬영장소명'],
                                                                                           row['촬영방향']))

                                                    # 확인 및 저장
                                                    path1 = car_json['Learning Data Info']['path']
                                                    json_path = 'C:/Users/MH46/Desktop/cctv55_완료/55_json/' + file.split('.')[0] + '.json'
                                                    with open(json_path, 'w', encoding='UTF-8') as outfile:
                                                        json.dump(car_json, outfile, indent=4, ensure_ascii=False)






