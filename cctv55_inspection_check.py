# 55. car exterior
# path 등 변수는 상황에 맞춰 수정하여 사용하였으니 코드 실행 전 확인 할 것

# 최종 json 검수

import os
import json
import re
import pandas as pd
import datetime


# path = "C:/Users/MH46/Desktop/cctv55_완료/55_json/"
# path = "C:/Users/MH46/Desktop/완성json_대기/55_json/"
# path = "C:/Users/MH46/Desktop/완성json_대기/이동완료/55_json/"
# path = "\\\\192.168.0.150\\완성데이터\\라벨링데이터\\차종외관인식\\"
# path = "\\\\192.168.0.150\\학습용데이터\\차종외관\\12월1주차\\"
# path = "D:/이동완료/55_json/"
path = "D:/완성데이터/라벨링데이터/차종외관인식/"
# path = "C:/Users/MH46/Desktop/완성데이터_오류수정/트레일러 오류 수정/"


num = 1
err_num = 1
err_num2 = 1
meta_check = pd.read_excel("C:/Users/MH46/Desktop/cctv55/55_Meta_check.xlsx")
err_list = pd.DataFrame(columns=['파일', '유형', '목록'])
st_car = pd.read_excel("C:/Users/MH46/Desktop/cctv55_완료/statistics/statistics.xlsx", sheet_name='car', index_col=0)
err_list2 = pd.DataFrame(columns=['파일', 'class_id', 'brand_id', 'model_id'])

# # 기본
# for i in os.listdir(path):
#     json_path = path + i

# 150 완성데이터
for (root, directory, files) in os.walk(path):
    if root.endswith('번'):
        for i in os.listdir(root):
            json_path = root + '/' + i

# # 150 학습데이터
# for (root, directory, files) in os.walk(path):
#     if root.endswith('라벨링데이터'):
#         for i in os.listdir(root):
#             json_path = root + '/' + i

            print("\n\n_______________검사대상 파일 : {} - {}_______________".format(num, i))

            if not re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{4}(.json)", i):
                print("파일명 오류 : {}".format(i))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, '파일명 오류', i]
                err_num += 1

            with open(json_path, 'r', encoding='UTF-8') as json_file:
                json_55 = json.load(json_file)

            # Raw Data Info 검사
            if json_55['Raw Data Info']['raw_data_id'] != i.split('_')[0] + '_' + i.split('_')[1] + '_' + i.split('_')[
                2] + '_' + i.split('_')[3]:
                print("raw_data_id 오류 : {}".format(json_55['Raw Data Info']['raw_data_id']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'raw_data_id 규칙 오류', json_55['Raw Data Info']['raw_data_id']]
                err_num += 1

            if json_55['Raw Data Info']['location_id'] != i.split('_')[2].lower():
                print("location_id 오류 : {}".format(json_55['Raw Data Info']['location_id']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'location_id 형식 오류', json_55['Raw Data Info']['location_id']]
                err_num += 1

            for index, row in meta_check.iterrows():
                if row['촬영장소'] == json_55['Raw Data Info']['location_id']:
                    if json_55['Raw Data Info']['location_name'] != row['촬영장소명']:
                        print("location_name 오류 : {}".format(json_55['Raw Data Info']['location_name']))
                        err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'location_name 일치 오류',
                                                                     json_55['Raw Data Info']['location_name']]
                        err_num += 1
            if json_55['Raw Data Info']['cctv_number'] != str(i.split('_')[3]):
                json_55['Raw Data Info']['cctv_number'] = str(i.split('_')[3])
                print("cctv_number/ 파일명 일치 오류 : {}".format(json_55['Raw Data Info']['cctv_number']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'cctv_number,파일명 일치 오류',
                                                             json_55['Raw Data Info']['cctv_number']]
                err_num += 1

            if type(json_55['Raw Data Info']['cctv_number']) != str:
                print("cctv_number 오류 : {}".format(json_55['Raw Data Info']['cctv_number']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'cctv_number 데이터 타입 오류',
                                                             json_55['Raw Data Info']['cctv_number']]
                err_num += 1

            if json_55['Raw Data Info']['copyrighter'] != "(주)미디어그룹사람과숲":
                print("copyrighter 오류 : {}".format(json_55['Raw Data Info']['copyrighter']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'copyrighter 일치 오류', json_55['Raw Data Info']['copyrighter']]
                err_num += 1


            if type(json_55['Raw Data Info']['resolution']) == list:
                print("resolution type 오류 : {}".format(json_55['Raw Data Info']['resolution']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'resolution type 형식 오류', json_55['Raw Data Info']['resolution']]
                err_num += 1

            if type(json_55['Raw Data Info']['resolution']) != list:
                for j in json_55['Raw Data Info']['resolution']:
                    if type(j) != str:
                        print("resolution type 오류 : {}".format(json_55['Raw Data Info']['resolution']))
                        err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'resolution 데이터 타입 오류',
                                                                     json_55['Raw Data Info']['resolution']]
                        err_num += 1

            if json_55['Raw Data Info']['resolution'] not in ["1920, 1080", "3840, 2160"]:
                print("resolution 오류 : {}".format(json_55['Raw Data Info']['resolution']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'resolution type 형식 오류', json_55['Raw Data Info']['resolution']]
                err_num += 1

            if not re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", json_55['Raw Data Info']['date']):
                print("date 오류 : {}".format(json_55['Raw Data Info']['date']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'date 형식 오류', json_55['Raw Data Info']['date']]
                err_num += 1

            if json_55['Raw Data Info']['start_time'].split(':')[0] != i.split('_')[1]:
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'start_time/파일명 일치 오류',
                                                             json_55['Raw Data Info']['start_time']]
                print("start_time/파일명 일치 오류 : {}".format(json_55['Raw Data Info']['start_time']))
                err_num += 1
                # aa = int(i.split('_')[1])
                # json_55['Raw Data Info']['start_time'] = '%02d' % aa + ':00:00'
                # json_55['Raw Data Info']['end_time'] = '%02d' % (aa + 1) + ':00:00'

            if json_55['Source Data Info']['extract_time'].split(':')[0] != i.split('_')[1]:
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'extract_time/파일명 일치 오류',
                                                             json_55['Source Data Info']['extract_time']]
                print("extract_time/파일명 일치 오류 : {}".format(json_55['Source Data Info']['extract_time']))
                err_num += 1
                # aa = ':' + json_55['Source Data Info']['extract_time'].split(':')[1] + ':' + \
                #      json_55['Source Data Info']['extract_time'].split(':')[2]
                # json_55['Source Data Info']['extract_time'] = i.split('_')[1] + aa

            if type(json_55['Raw Data Info']['start_time']) != str:
                print("start_time type 오류 : {}".format(json_55['Raw Data Info']['start_time']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'start_time 데이터 타입 오류',
                                                             json_55['Raw Data Info']['start_time']]
                err_num += 1

            if type(json_55['Raw Data Info']['start_time']) == str:
                if not re.match("[0-9]{2}:[0-9]{2}:[0-9]{2}", json_55['Raw Data Info']['start_time']):
                    print("start_time 오류 : {}".format(json_55['Raw Data Info']['start_time']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'start_time 형식 오류', json_55['Raw Data Info']['start_time']]
                    err_num += 1

            if type(json_55['Raw Data Info']['end_time']) != str:
                print("end_time type 오류 : {}".format(json_55['Raw Data Info']['end_time']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'end_time 데이터 타입 오류', json_55['Raw Data Info']['end_time']]
                err_num += 1

            if type(json_55['Raw Data Info']['end_time']) == str:
                if not re.match("[0-9]{2}:[0-9]{2}:[0-9]{2}", json_55['Raw Data Info']['end_time']):
                    print("end_time 오류 : {}".format(json_55['Raw Data Info']['end_time']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'end_time 형식 오류', json_55['Raw Data Info']['end_time']]
                    err_num += 1

            if json_55['Raw Data Info']['start_time'] == "12:00:00":
                if json_55['Raw Data Info']['end_time'] == "01:00:00":
                    json_55['Raw Data Info']['end_time'] = "13:00:00"
                    print("start_time, end_time 오류 : {}, {}".format(json_55['Raw Data Info']['start_time'],
                                                                    json_55['Raw Data Info']['end_time']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'start_time, end_time 오류',
                                                                 json_55['Raw Data Info']['end_time']]
                    err_num += 1

            if json_55['Raw Data Info']['start_time'] == "":
                print("start_time NaN 오류")
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'start_time nan 오류', json_55['Raw Data Info']['start_time']]
                err_num += 1

            if json_55['Raw Data Info']['end_time'] == "":
                print("end_time NaN 오류")
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'end_time nan 오류', json_55['Raw Data Info']['end_time']]
                err_num += 1



            if json_55['Raw Data Info']['length'] != 3600:
                print("length 오류 : {}".format(json_55['Raw Data Info']['length']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'length 오류', json_55['Raw Data Info']['length']]
                err_num += 1

            if json_55['Raw Data Info']['fps'] != 30:
                print("fps 오류 : {}".format(json_55['Raw Data Info']['fps']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'fps 형식 오류', json_55['Raw Data Info']['fps']]
                err_num += 1

            if (json_55['Raw Data Info']['date'] >= '2022-06-01') and (json_55['Raw Data Info']['date'] <= '2022-08-31'):
                if json_55['Raw Data Info']['season'] != 'su':
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'season 오류', '{}, {}'.format(json_55['Raw Data Info']['season'], json_55['Raw Data Info']['date'])]
                    err_num += 1
                    print("season 오류 : {}, {}".format(json_55['Raw Data Info']['season'], json_55['Raw Data Info']['date']))
                    # json_55['Raw Data Info']['season'] = 'su'

            if (json_55['Raw Data Info']['date'] >= '2022-09-01') and (json_55['Raw Data Info']['date'] <= '2022-11-30'):
                if json_55['Raw Data Info']['season'] != 'fa':
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'season 오류', '{}, {}'.format(json_55['Raw Data Info']['season'], json_55['Raw Data Info']['date'])]
                    err_num += 1
                    print("season 오류 : {}, {}".format(json_55['Raw Data Info']['season'], json_55['Raw Data Info']['date']))
                    # json_55['Raw Data Info']['season'] = 'fa'

            if (json_55['Raw Data Info']['date'] >= '2022-12-01') and (json_55['Raw Data Info']['date'] <= '2022-12-31'):
                if json_55['Raw Data Info']['season'] != 'wi':
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'season 오류', '{}, {}'.format(json_55['Raw Data Info']['season'], json_55['Raw Data Info']['date'])]
                    err_num += 1
                    print("season 오류 : {}, {}".format(json_55['Raw Data Info']['season'], json_55['Raw Data Info']['date']))
                    # json_55['Raw Data Info']['season'] = 'wi'

            if json_55['Raw Data Info']['season'] not in ['su', 'fa']:
                print("season 오류 : {}".format(json_55['Raw Data Info']['season']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'season 오류', json_55['Raw Data Info']['season']]
                err_num += 1

            if json_55['Raw Data Info']['weather'] not in ['s', 'r', 'f', 'n']:
                print("weather 오류 : {}".format(json_55['Raw Data Info']['weather']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'weather 오류', json_55['Raw Data Info']['weather']]
                err_num += 1

            if json_55['Raw Data Info']['day_type'] not in ['w', 'h']:
                print("day_type 오류 : {}".format(json_55['Raw Data Info']['day_type']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'day_type 오류', json_55['Raw Data Info']['day_type']]
                err_num += 1

            if json_55['Raw Data Info']['road_type'] not in ['cr', 'sr', 'ar']:
                print("road_type 오류 : {}".format(json_55['Raw Data Info']['road_type']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'road_type 오류', json_55['Raw Data Info']['road_type']]
                err_num += 1

            if json_55['Raw Data Info']['road_type'] != "cr":
                if json_55['Raw Data Info']['cross_type'] != "":
                    print("cross_type 오류 : {}".format(json_55['Raw Data Info']['cross_type']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'cross_type ar,sr 경우 nan 오류',
                                                                 json_55['Raw Data Info']['cross_type']]
                    err_num += 1

            if json_55['Raw Data Info']['road_type'] == "cr":
                if json_55['Raw Data Info']['cross_type'] not in ['f3', 'f4', 'sl', 'ul', 'rl']:
                    print("cross_type 오류 : {}".format(json_55['Raw Data Info']['cross_type']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'cross_type cr 경우 데이터 오류',
                                                                 json_55['Raw Data Info']['cross_type']]
                    err_num += 1

            if type(json_55['Raw Data Info']['cctv_type']) != int:
                print("cctv_type 오류 : {}".format(json_55['Raw Data Info']['cctv_type']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'cctv_type 데이터 타입 오류', json_55['Raw Data Info']['cctv_type']]
                err_num += 1

            if json_55['Raw Data Info']['lens_type'] not in ['wa', 'na', 'sa']:
                print("lens_type 오류 : {}".format(json_55['Raw Data Info']['lens_type']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'lens_type 데이터 오류', json_55['Raw Data Info']['lens_type']]
                err_num += 1

            if type(json_55['Raw Data Info']['cctv_height']) != int:
                print("cctv_height 오류 : {}".format(json_55['Raw Data Info']['cctv_height']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'cctv_height 데이터 타입 오류',
                                                             json_55['Raw Data Info']['cctv_height']]
                err_num += 1

            if type(json_55['Raw Data Info']['cctv_angle']) != int:
                print("cctv_angle 오류 : {}".format(json_55['Raw Data Info']['cctv_angle']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'cctv_angle 데이터 타입 오류', json_55['Raw Data Info']['cctv_angle']]
                err_num += 1

            if type(json_55['Raw Data Info']['cctv_gps']) != list:
                print("cctv_gps type 오류 : {}".format(json_55['Raw Data Info']['cctv_gps']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'cctv_gps 형식 오류', json_55['Raw Data Info']['cctv_gps']]
                err_num += 1

            if type(json_55['Raw Data Info']['cctv_gps']) == list:
                for j in json_55['Raw Data Info']['cctv_gps']:
                    if type(j) != float:
                        print("cctv_gps type 오류 : {}".format(json_55['Raw Data Info']['cctv_gps']))
                        err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'cctv_gps 데이터 타입 오류',
                                                                     json_55['Raw Data Info']['cctv_gps']]
                        err_num += 1

            if json_55['Raw Data Info']['file_extension'] != 'mp4':
                print("file_extension 오류 : {}".format(json_55['Raw Data Info']['file_extension']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'file_extension 데이터 오류',
                                                             json_55['Raw Data Info']['file_extension']]
                err_num += 1

            # Source Data Info 검사
            if json_55['Source Data Info']['source_data_id'] != i.split('.')[0]:
                print("source_data_id 오류 : {}".format(json_55['Source Data Info']['source_data_id']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'source_data_id 오류',
                                                             json_55['Source Data Info']['source_data_id']]
                err_num += 1

            if json_55['Source Data Info']['classification_id'] != "a":
                print("classification_id 오류 : {}".format(json_55['Source Data Info']['classification_id']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'classification_id 데이터 오류',
                                                             json_55['Source Data Info']['classification_id']]
                err_num += 1

            if type(json_55['Source Data Info']['extract_time']) != str:
                print("extract_time type 오류 : {}".format(json_55['Source Data Info']['extract_time']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'extract_time 데이터 타입 오류',
                                                             json_55['Source Data Info']['extract_time']]
                err_num += 1

            if type(json_55['Source Data Info']['extract_time']) == str:
                if not re.match("[0-9]{2}:[0-9]{2}:[0-9]{2}", json_55['Source Data Info']['extract_time']):
                    print("extract_time 오류 : {}".format(json_55['Source Data Info']['extract_time']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'extract_time 형식 오류',
                                                                 json_55['Source Data Info']['extract_time']]
                    err_num += 1

            if json_55['Source Data Info']['file_extension'] != "jpg":
                print("Source file_extension 오류 : {}".format(json_55['Source Data Info']['file_extension']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'file_extension 데이터 오류',
                                                             json_55['Source Data Info']['file_extension']]
                err_num += 1

            # Learning Data Info 검사
            if json_55['Raw Data Info']['road_type'] == 'cr':
                path_name = '교차로'
                if json_55['Learning Data Info']['path'] != '/차종외관인식/{}/[{}]{}/{}번'.format(path_name,
                                                                                   json_55['Raw Data Info']['location_id'],
                                                                                   json_55['Raw Data Info']['location_name'],
                                                                                   json_55['Raw Data Info']['cctv_number']):
                    print("path 오류 : {}".format(json_55['Learning Data Info']['path']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'path cr 오류', json_55['Learning Data Info']['path']]
                    # json_55['Learning Data Info']['path'] = '/차종외관인식/{}/[{}]{}/{}번'.format(path_name,
                    #                                                                         json_55[
                    #                                                                             'Raw Data Info'][
                    #                                                                             'location_id'],
                    #                                                                         json_55[
                    #                                                                             'Raw Data Info'][
                    #                                                                             'location_name'],
                    #                                                                         json_55[
                    #                                                                             'Raw Data Info'][
                    #                                                                             'cctv_number'])
                    err_num += 1

            if json_55['Raw Data Info']['road_type'] == 'sr':
                path_name = '이면도로'
                if json_55['Learning Data Info']['path'] != '/차종외관인식/{}/[{}]{}/{}번'.format(path_name,
                                                                                   json_55['Raw Data Info']['location_id'],
                                                                                   json_55['Raw Data Info']['location_name'],
                                                                                   json_55['Raw Data Info']['cctv_number']):
                    print("path 오류 : {}".format(json_55['Learning Data Info']['path']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'path sr 오류', json_55['Learning Data Info']['path']]
                    # json_55['Learning Data Info']['path'] = '/차종외관인식/{}/[{}]{}/{}번'.format(path_name,
                    #                                                                         json_55[
                    #                                                                             'Raw Data Info'][
                    #                                                                             'location_id'],
                    #                                                                         json_55[
                    #                                                                             'Raw Data Info'][
                    #                                                                             'location_name'],
                    #                                                                         json_55[
                    #                                                                             'Raw Data Info'][
                    #                                                                             'cctv_number'])
                    err_num += 1

            if json_55['Raw Data Info']['road_type'] == 'ar':
                path_name = '접근로'
                if json_55['Learning Data Info']['path'] != '/차종외관인식/{}/[{}]{}/{}번'.format(path_name,
                                                                                   json_55['Raw Data Info']['location_id'],
                                                                                   json_55['Raw Data Info']['location_name'],
                                                                                   json_55['Raw Data Info']['cctv_number']):
                    print("path 오류 : {}".format(json_55['Learning Data Info']['path']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'path ar 오류', json_55['Learning Data Info']['path']]
                    # json_55['Learning Data Info']['path'] = '/차종외관인식/{}/[{}]{}/{}번'.format(path_name,
                    #                                                                         json_55[
                    #                                                                             'Raw Data Info'][
                    #                                                                             'location_id'],
                    #                                                                         json_55[
                    #                                                                             'Raw Data Info'][
                    #                                                                             'location_name'],
                    #                                                                         json_55[
                    #                                                                             'Raw Data Info'][
                    #                                                                             'cctv_number'])
                    err_num += 1

            if json_55['Learning Data Info']['json_data_id'] != i.split('.')[0]:
                print("json_data_id 오류 : {}".format(json_55['Learning Data Info']['json_data_id']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'json_data_id 오류',
                                                             json_55['Learning Data Info']['json_data_id']]
                err_num += 1

            if json_55['Learning Data Info']['file_extension'] != 'json':
                print("Learning file_extension 오류 : {}".format(json_55['Learning Data Info']['file_extension']))
                err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'file_extension 데이터 오류',
                                                             json_55['Learning Data Info']['file_extension']]
                err_num += 1

            for annotations in json_55['Learning Data Info']['annotations']:
                if annotations['class_id'] not in ["car-01", "car-02", "car-03", "car-04", "car-05", "car-06", "car-07"]:
                    print("class_id 오류 : {}".format(annotations['class_id']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'class_id 데이터 오류', annotations['class_id']]
                    err_num += 1

                if annotations['type'] != "bbox":
                    print("bbox type 오류 : {}".format(annotations['type']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'type:bbox 오류', annotations['path']]
                    err_num += 1

                if type(annotations['coord']) != list:
                    print("coord 오류 : {}".format(annotations['coord']))
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'coord 형식 오류', annotations['coord']]
                    err_num += 1

                if type(annotations['coord']) == list:
                    for j in annotations['coord']:
                        if type(j) != float:
                            print("coord type 오류 : {}".format(annotations['coord']))
                            err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'type:bbox 오류', annotations['path']]
                            err_num += 1

                if annotations['model_id'].find('Unkonwn') != -1:
                    print(annotations['model_id'])
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id Unknown 오류', annotations['model_id']]
                    annotations['model_id'] = annotations['model_id'].replace('Unkonwn', 'Unknown')
                    err_num += 1

                if annotations['model_id'].find('unknown') != -1:
                    print(annotations['model_id'])
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id Unknown 오류', annotations['model_id']]
                    annotations['model_id'] = annotations['model_id'].replace('Unknown', 'Unknown')
                    err_num += 1

                if annotations['model_id'].find('Unknwon') != -1:
                    print(annotations['model_id'])
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id Unknown 오류', annotations['model_id']]
                    annotations['model_id'] = annotations['model_id'].replace('Unknwon', 'Unknown')
                    err_num += 1

                if annotations['brand_id'].find('Unkonwn') != -1:
                    print(annotations['brand_id'])
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'brand_id Unknown 오류', annotations['brand_id']]
                    annotations['brand_id'] = annotations['brand_id'].replace('Unkonwn', 'Unknown')
                    err_num += 1

                if annotations['brand_id'].find('Unknwon') != -1:
                    print(annotations['brand_id'])
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'brand_id Unknown 오류', annotations['brand_id']]
                    annotations['brand_id'] = annotations['brand_id'].replace('Unknwon', 'Unknown')
                    err_num += 1

                if annotations['brand_id'] == "버스":
                    err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'brand_id 버스 오류/수정', annotations['brand_id']]
                    print("brand_id / model_id 오류 : {}, {}".format(annotations['brand_id'], annotations['model_id']))
                    annotations['brand_id'] = annotations['model_id']
                    annotations['model_id'] = "Unknown"
                    print("brand_id / model_id 수정 : {}, {}".format(annotations['brand_id'], annotations['model_id']))
                    err_num += 1

                # # 차종 수정
                # if annotations['class_id'] == "car-01":
                #     if annotations['brand_id'] == "쉐보레":
                #         print("brand_id 차종 수정 : {}".format(annotations['brand_id']))
                #         err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'brand_id 차종 오류/수정', annotations['brand_id']]
                #         annotations['brand_id'] = "쉐보레(GM대우)"
                #         err_num += 1
                #
                # if annotations['brand_id'] == "ETC":
                #     print("brand_id 차종 수정 : {}".format(annotations['brand_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'brand_id 차종 오류/수정', annotations['brand_id']]
                #     annotations['brand_id'] = "Unknown"
                #     err_num += 1
                #
                # if annotations['class_id'] == "car-04":
                #     if annotations['brand_id'] == "쉐보레":
                #         print("brand_id 차종 수정 : {}".format(annotations['brand_id']))
                #         err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'brand_id 차종 오류/수정', annotations['brand_id']]
                #         annotations['brand_id'] = "타타대우"
                #         err_num += 1
                # if annotations['class_id'] == "car-04":
                #     if annotations['brand_id'] == "만":
                #         print("brand_id 차종 수정 : {}".format(annotations['brand_id']))
                #         err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'brand_id 차종 오류/수정', annotations['brand_id']]
                #         annotations['brand_id'] = "만(MAN)"
                #         err_num += 1
                #
                # if annotations['brand_id'] == "매뉴얼바이크":
                #     print("brand_id 차종 수정 : {}".format(annotations['brand_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'brand_id 차종 오류/수정', annotations['brand_id']]
                #     annotations['brand_id'] = "매뉴얼바이크(수동)"
                #     err_num += 1
                #
                # if annotations['brand_id'] == "스쿠터":
                #     print("brand_id 차종 수정 : {}".format(annotations['brand_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'brand_id 차종 오류/수정', annotations['brand_id']]
                #     annotations['brand_id'] = "스쿠터(자동)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "1시리즈 _F40(2020)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "1시리즈_F40(2020)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "1시리즈 _F20(2012)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "1시리즈_F20(2012)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "2시리즈 _F44(2020)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "2시리즈_F44(2020)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "2시리즈 _F45(2015)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "2시리즈_F45(2015)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "3시리즈 _G20(2019)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "3시리즈_G20(2019)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "팰리세이드_펠리세이드(2018)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "펠리세이드_펠리세이드(2018)"
                #     err_num += 1
                #
                # if (annotations['model_id'] == "3시리즈_ F30(2012)") or (annotations['model_id'] == "3시리즈 _F30(2012)"):
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "3시리즈_F30(2012)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "4시리즈_ G22(2021)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "4시리즈_G22(2021)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "4시리즈 _F32(2013)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "4시리즈_F32(2013)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "5시리즈 _F10(2010)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "5시리즈_F10(2010)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "5시리즈 _G30(2017)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "5시리즈_G30(2017)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "6시리즈_ F12(2011)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "6시리즈_F12(2011)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "7시리즈_ G11(2015)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "7시리즈_G11(2015)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "7시리즈_ F01(2008)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "7시리즈_F01(2008)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "7시리즈_ E65(2002)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "7시리즈_E65(2002)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "K3_더 뉴 (2015)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "K3_더 뉴(2015)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "K5_더 뉴 2세대(2018)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "K5_2세대(2015)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "모닝_올 뉴(JA),어반(2017)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "모닝_어반(2020)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "K3_더 뉴 2세대 (2021)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "K3_더 뉴 2세대(2021)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "익스플로러_6세대(1991)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "익스플로러_6세대(2019)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "모닝_올 뉴,더 뉴(2011)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "모닝_올 뉴(2011)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "모하비_더 뉴(2016)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "모하비_모하비(2007)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "스포티지_스포티지(2004)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "스포티지_뉴(2004)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "프라이드_프라이드(신형)(2005)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "프라이드_신형(2005)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "ES_뉴 제너레이션 (2018)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "ES_뉴 제너레이션(2018)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "SM5_노버(2015)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "SM5_노바(2015)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "XC90_올 뉴 (2016)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "XC90_올 뉴(2016)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "아베오_세단(2011)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "아베오_아베오(2011)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "라세티_프리미어(2008)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "말리부_말리부(2011)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "코란도_뉴 스타일(2017)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "코란도_뉴 스타일 C(2017)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "A5_F5(2017)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "A5_A5(2007)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "Q5_FY(2017)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "Q5_Q5(2008)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "그랜저_IG(더 뉴)(2016)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "그랜저_IG(2016)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "그랜저_XG (2002)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "그랜저_XG(2002)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "스타렉스_그랜드 (2007)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "스타렉스_그랜드(2007)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "로체_어드밴스(2007)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "로체_로체(2005)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "i30_신형, 더 뉴(2011)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "i30_신형(2011)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "아이오닉_아이오닉 5(2021)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "아이오닉_5(2021)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "에쿠스_에쿠스(신형)(2009)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "에쿠스_신형(2009)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "봉고 3":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "봉고_봉고 Ⅲ(Unknown)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "봉고 프론티어":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "봉고_프론티어(Unknown)"
                #     err_num += 1
                #
                # if (annotations['model_id'] == "SM3_뉴제네레이션(2006)") or (annotations['model_id'] == "SM3_뉴 제네레이션(2006)"):
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "SM3_뉴제너레이션(2005)"
                #     err_num += 1
                #
                # if (annotations['model_id'] == "SM3_뉴제너레이션(2006)") or (annotations['model_id'] == "SM3_뉴 제너레이션(2006)"):
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "SM3_뉴제너레이션(2005)"
                #     err_num += 1
                #
                # if (annotations['model_id'] == "SM3_뉴제네레이션(2005)") or (annotations['model_id'] == "SM3_뉴 제네레이션(2005)"):
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "SM3_뉴제너레이션(2005)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "SM3_뉴 제너레이션(2005)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "SM3_뉴제너레이션(2005)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "ES_ES(1991)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "ES_ES(2001)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "LS_LS(1989)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "LS_LS(2006)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "랭글러_랭글러(1987)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "랭글러_랭글러(1996)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "체로키_체로키(1984)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "체로키_체로키(2002)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "익스플로러_5세대(1991)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "익스플로러_5세대(2010)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "어코드_어코드(1976)":
                #     print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #     err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 차종 오류/수정', annotations['model_id']]
                #     annotations['model_id'] = "어코드_어코드(2002)"
                #     err_num += 1
                #
                # if annotations['model_id'] == "메가트럭":
                #     if annotations['class_id'] != 'car-03':
                #         print("메가트럭 차종 수정 : {}".format(annotations['class_id']))
                #         err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id 메가트럭 오류/수정', annotations['model_id']]
                #         annotations['class_id'] = "car-03"
                #         err_num += 1
                #
                # if annotations['class_id'] == "car-04":
                #     if annotations['brand_id'] == "Unknown":
                #         if annotations['model_id'] != "Unknown":
                #             print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #             err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id Unknown 오류/수정', annotations['model_id']]
                #             annotations['model_id'] = "Unknown"
                #             err_num += 1
                #
                # if annotations['class_id'] == "car-05":
                #     if annotations['brand_id'] == "Unknown":
                #         if annotations['model_id'] != "Unknown":
                #             print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #             err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id Unknown 오류/수정', annotations['model_id']]
                #             annotations['model_id'] = "Unknown"
                #             err_num += 1
                #
                # if annotations['class_id'] == "car-05":
                #     if annotations['brand_id'] == "트레일러":
                #         if annotations['model_id'] == "Unknown":
                #             print("model_id 차종 수정 : {}".format(annotations['model_id']))
                #             err_list.loc[err_num, ['파일', '유형', '목록']] = [i, 'model_id Unknown 오류/수정', annotations['brand_id']]
                #             annotations['model_id'] = "트레일러"
                #             err_num += 1


                model = st_car['model_id'].values.tolist()
                brand = st_car[(st_car['model_id'] == annotations['model_id']) & (st_car['brand_id'] == annotations['brand_id'])]
                class_id = st_car[(st_car['model_id'] == annotations['model_id']) & (st_car['class_id'] == annotations['class_id'])]

                if annotations['model_id'] in model:
                    if len(brand) == 0:
                        err_list2.loc[err_num2, ['파일', '유형', 'class_id', 'brand_id', 'model_id']] = [i, 'brand_id 오류', annotations['class_id'], annotations['brand_id'], annotations['model_id']]
                        err_num2 += 1
                    if len(class_id) == 0:
                        err_list2.loc[err_num2, ['파일', '유형', 'class_id', 'brand_id', 'model_id']] = [i, 'class_id 오류', annotations['class_id'], annotations['brand_id'], annotations['model_id']]
                        err_num2 += 1
                if annotations['model_id'] not in model:
                    err_list2.loc[err_num2, ['파일', '유형', 'class_id', 'brand_id', 'model_id']] = [i, 'model_id 오류', annotations['class_id'], annotations['brand_id'],annotations['model_id']]
                    err_num2 += 1

                with open(json_path, 'w', encoding='UTF-8') as outfile:
                    json.dump(json_55, outfile, indent=4, ensure_ascii=False)

    num += 1



d_today = datetime.date.today()
today = d_today.strftime('%m%d')
filename = "{}_최종_inspection_check.xlsx".format(today)
err_path = 'C:/Users/MH46/Desktop/cctv55/err_list/{}'.format(filename)

print(err_list)
print(err_list2)

with pd.ExcelWriter(err_path) as writer:
    err_list.to_excel(writer, sheet_name='메타', startrow=0 ,startcol=0)
    err_list2.to_excel(writer, sheet_name='차종', startrow=0 ,startcol=0)

