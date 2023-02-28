# 55. car exterior
# path 등 변수는 상황에 맞춰 수정하여 사용하였으니 코드 실행 전 확인 할 것

# 통계

import json
import pandas as pd
import os
import datetime
import shutil
import re
import random


# path = "C:/Users/MH46/Desktop/cctv55_완료/55_json/"
# path = "C:/Users/MH46/Desktop/완성json_대기/55_json/"
# path = "C:/Users/MH46/Desktop/완성json_대기/이동완료/55_json/"
path = "D:/완성데이터/라벨링데이터/차종외관인식/"
# path = "\\\\192.168.0.150\\완성데이터\\라벨링데이터\\차종외관인식\\"
# path = "\\\\192.168.0.150\\학습용데이터\\차종외관\\"


meta_xlsx = pd.DataFrame \
    (columns=['구분', '원시 파일명' ,'촬영장소', '촬영방향', '촬영장소명', '해상도', '촬영일시\n(yyyy-mm-dd)', '촬영 시작 시간', '촬영 종료 시간',	'영상길이(초) [고정]',	'FPS\n[고정]', '계절',
                                  '날씨', '평일/주말/휴일', '도로 유형', '교차로 유형', 'CCTV 카메라 유형',	'CCTV 렌즈\n유형', 'CCTV 설치높이', 'CCTV 각도', 'CCTV GPS정보', '추출시간\n(hh:mm:ss)', '파일명'])
meta_xlsx = meta_xlsx.set_index('구분')
a = 1
num = 1
d_today = datetime.date.today()
today = d_today.strftime('%m%d')
st = pd.read_excel("C:/Users/MH46/Desktop/cctv55_완료/statistics/statistics.xlsx", sheet_name='통계', index_col=0)
st_car = pd.read_excel("C:/Users/MH46/Desktop/cctv55_완료/statistics/statistics.xlsx", sheet_name='car', index_col=0)
st_road = pd.read_excel("C:/Users/MH46/Desktop/cctv55_완료/statistics/statistics.xlsx", sheet_name='road', index_col=0)
st_time = pd.read_excel("C:/Users/MH46/Desktop/cctv55_완료/statistics/statistics.xlsx", sheet_name='time', index_col=0)

st_err = pd.DataFrame(columns = ['유형', '파일명'])
st_car[today] = 0
st_road[today] = 0
st.loc[today] = 0
st_time[today] = 0
road_list = []
brand_list = []
model_list = []
start_list = []
end_list = []

for i in st_road['촬영장소']:
    road_list.append(i)
for i in st_car['brand_id']:
    brand_list.append(i)
for i in st_car['model_id']:
    model_list.append(i)
for i in st_time['start_time']:
    start_list.append(i)
for i in st_time['end_time']:
    end_list.append(i)


# # 일반
# for path_name in os.listdir(path):
#     with open(path + path_name, 'r', encoding='UTF-8') as json_file:
#         coco_json = json.load(json_file)

# 150 완성
for (root, directory, files) in os.walk(path):
    if root.endswith('번'):
    # if root.endswith('라벨링 데이터'):
        for i in os.listdir(root):
            with open(root + '\\' + i, 'r', encoding='UTF-8') as json_file:
                coco_json = json.load(json_file)

                meta_xlsx.loc[a] = [coco_json['Raw Data Info']['raw_data_id'], coco_json['Raw Data Info']['location_id'], coco_json['Raw Data Info']['cctv_number'], coco_json['Raw Data Info']['location_name'],
                                    [1920, 1080], coco_json['Raw Data Info']['date'], coco_json['Raw Data Info']['start_time'], coco_json['Raw Data Info']['end_time'], 3600, 30,
                                    coco_json['Raw Data Info']['season'], coco_json['Raw Data Info']['weather'], coco_json['Raw Data Info']['day_type'], coco_json['Raw Data Info']['road_type'],
                                    coco_json['Raw Data Info']['cross_type'], coco_json['Raw Data Info']['cctv_type'], coco_json['Raw Data Info']['lens_type'], coco_json['Raw Data Info']['cctv_height'],
                                    coco_json['Raw Data Info']['cctv_angle'], coco_json['Raw Data Info']['cctv_gps'], coco_json['Source Data Info']['extract_time'], coco_json['Source Data Info']['source_data_id']]
                a += 1

                print(meta_xlsx)




file_name = []
file_path = []
task_name = []


Ex55 = meta_xlsx

pd.to_datetime(Ex55['추출시간\n(hh:mm:ss)'], format="%H:%M:%S")



su = Ex55[Ex55['계절'] == 'su']['계절'].count()
fa = Ex55[Ex55['계절'] == 'fa']['계절'].count()
s = Ex55[Ex55['날씨'] == 's']['날씨'].count()
r = Ex55[Ex55['날씨'] == 'r']['날씨'].count()
f = Ex55[Ex55['날씨'] == 'f']['날씨'].count()
su_time1 = Ex55[((Ex55['계절'] == 'su') & ((Ex55['추출시간\n(hh:mm:ss)'] >= '05:30:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '06:30:00')))]['계절'].count()
su_time2 = Ex55[((Ex55['계절'] == 'su')) & ((Ex55['추출시간\n(hh:mm:ss)'] >= '19:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '20:00:00'))]['계절'].count()
fa_time1 = Ex55[((Ex55['계절'] == 'fa')) & ((Ex55['추출시간\n(hh:mm:ss)'] >= '06:30:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '07:30:00'))]['계절'].count()
fa_time2 = Ex55[((Ex55['계절'] == 'fa')) & ((Ex55['추출시간\n(hh:mm:ss)'] >= '19:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '20:00:00'))]['계절'].count()
su_time = su_time1 + su_time2
fa_time = fa_time1 + fa_time2
day = Ex55[(Ex55['추출시간\n(hh:mm:ss)'] >= '07:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '09:00:00')]['추출시간\n(hh:mm:ss)'].count()
night = Ex55[(Ex55['추출시간\n(hh:mm:ss)'] >= '17:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '19:00:00')]['추출시간\n(hh:mm:ss)'].count()
on = day + night
off = (su + fa) - on

st.loc[today, 'su'] = su
st.loc[today, 'fa'] = fa
st.loc[today, 's'] = s
st.loc[today, 'r'] = r
st.loc[today, 'f'] = f
st.loc[today, 'su_time'] = su_time
st.loc[today, 'fa_time'] = fa_time
st.loc[today, '첨두'] = on
st.loc[today, '비첨두'] = off


a = []
car_01 = 0
car_02 = 0
car_03 = 0
car_04 = 0
car_05 = 0
car_06 = 0
car_07 = 0
#
# # 일반
# for json_name in os.listdir(path):
#     with open(path + json_name, 'r', encoding='UTF-8') as json_file:
#         coco_json = json.load(json_file)

# 150 완성
for (root, directory, files) in os.walk(path):
    if root.endswith('번'):
    # if root.endswith('라벨링 데이터'):
        for json_name in os.listdir(root):
            with open(root + '\\' + json_name, 'r', encoding='UTF-8') as json_file:
                coco_json = json.load(json_file)


                if coco_json['Raw Data Info']['location_id'] in road_list:
                    st_road.loc[(st_road['촬영장소'] == coco_json['Raw Data Info']['location_id']), today] += 1
                if coco_json['Raw Data Info']['location_id'] not in road_list:
                    st_err.loc[num, '유형'] = "location_id : {}".format(coco_json['Raw Data Info']['location_id'])
                    st_err.loc[num, '파일명'] = json_name
                    print("location_id : {}".format(coco_json['Raw Data Info']['location_id']))
                    num += 1

                for start, end in zip(st_time['start_time'], st_time['end_time']):
                    if start == coco_json["Raw Data Info"]['start_time']:
                        if end == coco_json["Raw Data Info"]['end_time']:
                            if (coco_json['Source Data Info']['extract_time'] >= start) and (coco_json['Source Data Info']['extract_time'] < end):
                                st_time.loc[(st_time['start_time'] == start) & (st_time['end_time'] == end),today] += 1
                            else:
                                st_err.loc[num, '유형'] = "extract_time : {}".format(coco_json['Source Data Info']['extract_time'])
                                st_err.loc[num, '파일명'] = json_name
                                num += 1
                                print("extract_time : {}".format(coco_json['Source Data Info']['extract_time']))
                        if coco_json["Raw Data Info"]['end_time'] not in end_list:
                            st_err.loc[num, '유형'] = "end_time : {}".format(end)
                            st_err.loc[num, '파일명'] = json_name
                            num += 1
                            print("end_time : {}".format(end))
                    if coco_json["Raw Data Info"]['start_time'] not in start_list:
                        st_err.loc[num, '유형'] = "start_time : {}".format(start)
                        st_err.loc[num, '파일명'] = json_name
                        num += 1
                        print("start_time : {}".format(start))

                for j in coco_json['Learning Data Info']['annotations']:
                    if j['class_id'] == 'car-01':
                        car_01 += 1
                        if j['brand_id'] in brand_list:
                            if j['model_id'] in model_list:
                                st_car.loc[(st_car['class_id'] == j['class_id']) & (st_car['brand_id'] == j['brand_id']) & (st_car['model_id'] == j['model_id']),today] += 1
                            if j['model_id'] not in model_list:
                                st_err.loc[num, '유형'] = "model_id : {}".format(j['model_id'])
                                st_err.loc[num, '파일명'] = json_name
                                num += 1
                                print("model_id : {}".format(j['model_id']))
                        if j['brand_id'] not in brand_list:
                            st_err.loc[num, '유형'] = "brand_id : {}".format(j['brand_id'])
                            st_err.loc[num, '파일명'] = json_name
                            num += 1
                            print("brand_id : {}".format(j['brand_id']))

                    if j['class_id'] == 'car-02':
                        car_02 += 1
                        if j['brand_id'] in brand_list:
                            if j['model_id'] in model_list:
                                st_car.loc[(st_car['class_id'] == j['class_id']) & (st_car['brand_id'] == j['brand_id']) & (st_car['model_id'] == j['model_id']),today] += 1
                            if j['model_id'] not in model_list:
                                st_err.loc[num, '유형'] = "model_id : {}".format(j['model_id'])
                                st_err.loc[num, '파일명'] = json_name
                                num += 1
                                print("model_id : {}".format(j['model_id']))
                        if j['brand_id'] not in brand_list:
                            st_err.loc[num, '유형'] = "brand_id : {}".format(j['brand_id'])
                            st_err.loc[num, '파일명'] = json_name
                            num += 1
                            print("brand_id : {}".format(j['brand_id']))

                    if j['class_id'] == 'car-03':
                        car_03 += 1
                        if j['brand_id'] in brand_list:
                            if j['model_id'] in model_list:
                                st_car.loc[(st_car['class_id'] == j['class_id']) & (st_car['brand_id'] == j['brand_id']) & (st_car['model_id'] == j['model_id']),today] += 1
                            if j['model_id'] not in model_list:
                                st_err.loc[num, '유형'] = "model_id : {}".format(j['model_id'])
                                st_err.loc[num, '파일명'] = json_name
                                num += 1
                                print("model_id : {}".format(j['model_id']))
                        if j['brand_id'] not in brand_list:
                            st_err.loc[num, '유형'] = "brand_id : {}".format(j['brand_id'])
                            st_err.loc[num, '파일명'] = json_name
                            num += 1
                            print("brand_id : {}".format(j['brand_id']))

                    if j['class_id'] == 'car-04':
                        car_04 += 1
                        if j['brand_id'] in brand_list:
                            if j['model_id'] in model_list:
                                st_car.loc[(st_car['class_id'] == j['class_id']) & (st_car['brand_id'] == j['brand_id']) & (st_car['model_id'] == j['model_id']),today] += 1
                            if j['model_id'] not in model_list:
                                st_err.loc[num, '유형'] = "model_id : {}".format(j['model_id'])
                                st_err.loc[num, '파일명'] = json_name
                                num += 1
                                print("model_id : {}".format(j['model_id']))
                        if j['brand_id'] not in brand_list:
                            st_err.loc[num, '유형'] = "brand_id : {}".format(j['brand_id'])
                            st_err.loc[num, '파일명'] = json_name
                            num += 1
                            print("brand_id : {}".format(j['brand_id']))

                    if j['class_id'] == 'car-05':
                        car_05 += 1
                        if j['brand_id'] in brand_list:
                            if j['model_id'] in model_list:
                                st_car.loc[(st_car['class_id'] == j['class_id']) & (st_car['brand_id'] == j['brand_id']) & (st_car['model_id'] == j['model_id']),today] += 1
                            if j['model_id'] not in model_list:
                                st_err.loc[num, '유형'] = "model_id : {}".format(j['model_id'])
                                st_err.loc[num, '파일명'] = json_name
                                num += 1
                                print("model_id : {}".format(j['model_id']))
                        if j['brand_id'] not in brand_list:
                            st_err.loc[num, '유형'] = "brand_id : {}".format(j['brand_id'])
                            st_err.loc[num, '파일명'] = json_name
                            num += 1
                            print("brand_id : {}".format(j['brand_id']))
                        if j['brand_id'] == "Unknown":
                            st_err.loc[num, '유형'] = "car-05 : {}".format(j['brand_id'])
                            st_err.loc[num, '파일명'] = json_name
                            num += 1
                            print("brand_id : {}".format(j['brand_id']))


                    if j['class_id'] == 'car-06':
                        car_06 += 1
                        if j['brand_id'] in brand_list:
                            if j['model_id'] in model_list:
                                st_car.loc[(st_car['class_id'] == j['class_id']) & (st_car['brand_id'] == j['brand_id']) & (st_car['model_id'] == j['model_id']),today] += 1
                            if j['model_id'] not in model_list:
                                st_err.loc[num, '유형'] = "model_id : {}".format(j['model_id'])
                                st_err.loc[num, '파일명'] = json_name
                                num += 1
                                print("model_id : {}".format(j['model_id']))
                        if j['brand_id'] not in brand_list:
                            st_err.loc[num, '유형'] = "brand_id : {}".format(j['brand_id'])
                            st_err.loc[num, '파일명'] = json_name
                            num += 1
                            print("brand_id : {}".format(j['brand_id']))
                        if j['brand_id'] == "Unknown":
                            st_err.loc[num, '유형'] = "car-06 : {}".format(j['brand_id'])
                            st_err.loc[num, '파일명'] = json_name
                            num += 1
                            print("brand_id : {}".format(j['brand_id']))

                    if j['class_id'] == 'car-07':
                        car_07 += 1
                        if j['brand_id'] in brand_list:
                            if j['model_id'] in model_list:
                                st_car.loc[(st_car['class_id'] == j['class_id']) & (st_car['brand_id'] == j['brand_id']) & (st_car['model_id'] == j['model_id']),today] += 1
                            if j['model_id'] not in model_list:
                                st_err.loc[num, '유형'] = "model_id : {}".format(j['model_id'])
                                st_err.loc[num, '파일명'] = json_name
                                num += 1
                                print("model_id : {}".format(j['model_id']))
                        if j['brand_id'] not in brand_list:
                            st_err.loc[num, '유형'] = "brand_id : {}".format(j['brand_id'])
                            st_err.loc[num, '파일명'] = json_name
                            num += 1
                            print("brand_id : {}".format(j['brand_id']))

                    if j['class_id'] not in ['car-01', 'car-02', 'car-03', 'car-04', 'car-05', 'car-06', 'car-07']:
                        st_err.loc[num, '유형'] = "class_id : {}".format(j['class_id'])
                        st_err.loc[num, '파일명'] = json_name
                        num += 1
                        print("class_id : {}".format(j['class_id']))

                st.loc[today, 'car01'] = car_01
                st.loc[today, 'car02'] = car_02
                st.loc[today, 'car03'] = car_03
                st.loc[today, 'car04'] = car_04
                st.loc[today, 'car05'] = car_05
                st.loc[today, 'car06'] = car_06
                st.loc[today, 'car07'] = car_07

cr01_08 = Ex55['촬영장소'].isin(['cr01', 'cr02', 'cr03', 'cr04', 'cr05', 'cr06', 'cr07', 'cr08'])
ar01_08 = Ex55['촬영장소'].isin(['ar01', 'ar02', 'ar03', 'ar04', 'ar05', 'ar06', 'ar07', 'ar08'])
sr01_15 = Ex55['촬영장소'].isin(['sr01', 'sr02', 'sr03', 'sr04', 'sr05', 'sr06', 'sr07', 'sr08', 'sr09', 'sr10', 'sr11', 'sr12', 'sr13', 'sr14', 'sr15'])
cr13_18 = Ex55['촬영장소'].isin(['cr13', 'cr14', 'cr15', 'cr16', 'cr17', 'cr18'])
ar09 = Ex55['촬영장소'] == 'ar09'
cr11_12 = Ex55['촬영장소'].isin(['cr11', 'cr12'])

st.loc[today, '안양 교차로/07~12'] = 0
st.loc[today, '안양 교차로/12~17'] = 0
st.loc[today, '안양 교차로/17~24'] = 0
st.loc[today, '안양 교차로/00~07'] = 0

st.loc[today, '안양 접근로/07~12'] = 0
st.loc[today, '안양 접근로/12~17'] = 0
st.loc[today, '안양 접근로/17~24'] = 0
st.loc[today, '안양 접근로/00~07'] = 0

st.loc[today, '안양 이면도로/07~12'] = 0
st.loc[today, '안양 이면도로/12~17'] = 0
st.loc[today, '안양 이면도로/17~24'] = 0
st.loc[today, '안양 이면도로/00~07'] = 0

st.loc[today, '판교 교차로/07~12'] = 0
st.loc[today, '판교 교차로/12~17'] = 0
st.loc[today, '판교 교차로/17~24'] = 0
st.loc[today, '판교 교차로/00~07'] = 0

st.loc[today, '판교 접근로/07~12'] = 0
st.loc[today, '판교 접근로/12~17'] = 0
st.loc[today, '판교 접근로/17~24'] = 0
st.loc[today, '판교 접근로/00~07'] = 0

st.loc[today, '대구 교차로/07~12'] = 0
st.loc[today, '대구 교차로/12~17'] = 0
st.loc[today, '대구 교차로/17~24'] = 0
st.loc[today, '대구 교차로/00~07'] = 0

if Ex55[cr01_08]['추출시간\n(hh:mm:ss)'].count() >= 1:
    st.loc[today, '안양 교차로/07~12'] = st.loc[today, '안양 교차로/07~12'] + Ex55[cr01_08 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '07:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '12:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '안양 교차로/12~17'] = st.loc[today, '안양 교차로/12~17'] + Ex55[cr01_08 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '12:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '17:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '안양 교차로/17~24'] = st.loc[today, '안양 교차로/17~24'] + Ex55[cr01_08 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '17:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '24:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '안양 교차로/00~07'] = st.loc[today, '안양 교차로/00~07'] + Ex55[cr01_08 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '00:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '07:00:00'))]['추출시간\n(hh:mm:ss)'].count()

if Ex55[ar01_08]['추출시간\n(hh:mm:ss)'].count() >= 1:
    st.loc[today, '안양 접근로/07~12'] = st.loc[today, '안양 접근로/07~12'] + Ex55[ar01_08 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '07:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '12:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '안양 접근로/12~17'] = st.loc[today, '안양 접근로/12~17'] + Ex55[ar01_08 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '12:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '17:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '안양 접근로/17~24'] = st.loc[today, '안양 접근로/17~24'] + Ex55[ar01_08 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '17:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '24:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '안양 접근로/00~07'] = st.loc[today, '안양 접근로/00~07'] + Ex55[ar01_08 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '00:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '07:00:00'))]['추출시간\n(hh:mm:ss)'].count()

if Ex55[sr01_15]['추출시간\n(hh:mm:ss)'].count() >= 1:
    st.loc[today, '안양 이면도로/07~12'] = st.loc[today, '안양 이면도로/07~12'] + Ex55[sr01_15 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '07:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '12:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '안양 이면도로/12~17'] = st.loc[today, '안양 이면도로/12~17'] + Ex55[sr01_15 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '12:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '17:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '안양 이면도로/17~24'] = st.loc[today, '안양 이면도로/17~24'] + Ex55[sr01_15 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '17:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '24:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '안양 이면도로/00~07'] = st.loc[today, '안양 이면도로/00~07'] + Ex55[sr01_15 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '00:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '07:00:00'))]['추출시간\n(hh:mm:ss)'].count()

if Ex55[cr13_18]['추출시간\n(hh:mm:ss)'].count() >= 1:
    st.loc[today, '판교 교차로/07~12'] = st.loc[today, '판교 교차로/07~12'] + Ex55[cr13_18 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '07:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '12:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '판교 교차로/12~17'] = st.loc[today, '판교 교차로/12~17'] + Ex55[cr13_18 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '12:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '17:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '판교 교차로/17~24'] = st.loc[today, '판교 교차로/17~24'] + Ex55[cr13_18 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '17:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '24:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '판교 교차로/00~07'] = st.loc[today, '판교 교차로/00~07'] + Ex55[cr13_18 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '00:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '07:00:00'))]['추출시간\n(hh:mm:ss)'].count()

if Ex55[ar09]['추출시간\n(hh:mm:ss)'].count() >= 1:
    st.loc[today, '판교 접근로/07~12'] = st.loc[today, '판교 접근로/07~12'] + Ex55[ar09 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '07:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '12:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '판교 접근로/12~17'] = st.loc[today, '판교 접근로/12~17'] + Ex55[ar09 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '12:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '17:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '판교 접근로/17~24'] = st.loc[today, '판교 접근로/17~24'] + Ex55[ar09 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '17:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '24:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '판교 접근로/00~07'] = st.loc[today, '판교 접근로/00~07'] + Ex55[ar09 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '00:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '07:00:00'))]['추출시간\n(hh:mm:ss)'].count()

if Ex55[cr11_12]['추출시간\n(hh:mm:ss)'].count() >= 1:
    st.loc[today, '대구 교차로/07~12'] = st.loc[today, '대구 교차로/07~12'] + Ex55[cr11_12 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '07:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '12:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '대구 교차로/12~17'] = st.loc[today, '대구 교차로/12~17'] + Ex55[cr11_12 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '12:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '17:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '대구 교차로/17~24'] = st.loc[today, '대구 교차로/17~24'] + Ex55[cr11_12 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '17:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '24:00:00'))]['추출시간\n(hh:mm:ss)'].count()
    st.loc[today, '대구 교차로/00~07'] = st.loc[today, '대구 교차로/00~07'] + Ex55[cr11_12 & ((Ex55['추출시간\n(hh:mm:ss)'] >= '00:00:00') & (Ex55['추출시간\n(hh:mm:ss)'] < '07:00:00'))]['추출시간\n(hh:mm:ss)'].count()



st = st.fillna(0)

for i in st.columns:
    if st[i].dtype != int:
        st[i] = st[i].astype(int)

statistics = st




print(statistics)


with pd.ExcelWriter('C:/Users/MH46/Desktop/cctv55_완료/statistics/statistics.xlsx') as writer:
    statistics.to_excel(writer, sheet_name='통계', startrow=0 ,startcol=0)
    st_car.to_excel(writer, sheet_name='car')
    st_road.to_excel(writer, sheet_name='road')
    st_time.to_excel(writer, sheet_name='time')

with pd.ExcelWriter("C:/Users/MH46/Desktop/cctv55_완료/statistics/{}_최종_statistics_err.xlsx".format(today)) as writer:
    st_err.to_excel(writer, sheet_name='err')




