# path 등 변수는 상황에 맞춰 수정하여 사용하였으니 코드 실행 전 확인 할 것


import json
import pandas as pd
import os
import datetime
import shutil
import re
import random


# 경로 및 픽셀 검사
def coco_file_check():
    # coco json 불러오기
    ins_path = ''
    jpg_path = ''
    file_name_ins = os.listdir(ins_path)
    path = []
    err_list = pd.DataFrame(columns=['경로', '번호', 'x', 'y'])
    num = 1
    a_list = []

    for jpg_name in os.listdir(jpg_path):
        a_list.append(jpg_name)

    for jpg_name in os.listdir(jpg_path):
        if re.match("(C)-[0-9]{8}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", jpg_name):
            if jpg_name.split('-20')[0] + '-' + jpg_name.split('-20')[1] not in a_list:
                os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('-20')[0] + '-' + jpg_name.split('-20')[1])
        if re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{6}(.jpg)", jpg_name):
            a = jpg_name.split('.jpg')[0].split('_A')[1]
            if jpg_name.split('_A')[0] + '_A' + a[-4:] + '.jpg' not in a_list:
                os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('_A')[0] + '_A' + a[-4:] + '.jpg')
        if re.match("(C)-[0-9]{6}_[0-9]{2}_(CL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", jpg_name):
            os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('CL')[0] + 'CR' + jpg_name.split('CL')[1])
        if re.match("(C)-[0-9]{6}_[0-9]{2}_(SL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", jpg_name):
            os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('SL')[0] + 'SR' + jpg_name.split('SL')[1])
        if re.match("(C)-[0-9]{6}_[0-9]{2}_(AL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", jpg_name):
            os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('AL')[0] + 'AR' + jpg_name.split('AL')[1])
        if re.match("(C)-[0-9]{6}_(08.1)_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", jpg_name):
            os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('08.1')[0] + '08' + jpg_name.split('08.1')[1])
        if re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_N[0-9]{4}_[0-9]*(.jpg)", jpg_name):
            os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('_')[0] + '_' + jpg_name.split('_')[1] + '_' + jpg_name.split('_')[2] + '_' + jpg_name.split('_')[3] + '_' + jpg_name.split('_')[4] + '.jpg')
        if re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_N[0-9]*(.jpg)", jpg_name):
            os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('_N')[0] + '_A' + jpg_name.split('_N')[1])
        if re.match("(C)-(229713)_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", jpg_name):
            if jpg_name.split('229713')[0] + "220713" + jpg_name.split('229713')[1] not in a_list:
                os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('229713')[0] + "220713" + jpg_name.split('229713')[1])
        if re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{4}_[0-9]*(.jpg)", jpg_name):
            if jpg_name.split('_')[0] + '_' + jpg_name.split('_')[1] + '_' + jpg_name.split('_')[2] + '_' + jpg_name.split('_')[3] + '_' + jpg_name.split('_')[4] + '.jpg' not in a_list:
                os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('_')[0] + '_' + jpg_name.split('_')[1] + '_' + jpg_name.split('_')[2] + '_' + jpg_name.split('_')[3] + '_' + jpg_name.split('_')[4] + '.jpg')
        if re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_[0-9]*(.jpg)", jpg_name):
            os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('_')[0] + '_' + jpg_name.split('_')[1] + '_' + jpg_name.split('_')[2] + '_' + jpg_name.split('_')[3] + '_A' + jpg_name.split('_')[4])
        if re.match("(C)-[0-9]{6}_[0-9]{2}_(AR07)_(01)_A[0-9]*(.jpg)", jpg_name):
            os.rename(jpg_path + jpg_name, jpg_path + jpg_name.split('AR07_01')[0] + 'AR07_03' + jpg_name.split('AR07_01')[1])


    for i in file_name_ins:
        a = i.split('.')[0]
        os.rename(ins_path + '/' + a + '.json', ins_path + '/' + a.upper() + '.json')
        path.append(ins_path + '/' + a.upper() + '.json')

    for coco_path in path:
        print("______________________________생성 json 경로 : {}".format(coco_path))
        with open(coco_path, "r", encoding="UTF-8") as json_file:
            coco_json = json.load(json_file)


        for i in coco_json['images']:
            if re.match(".*/.*", str(i['file_name'])):
                i['file_name'] = i['file_name'].split('/')[1]

        for i in coco_json['images']:
            if re.match("(C)-[0-9]{8}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('-20')[0] + "-" + i['file_name'].split('-20')[1]
            if re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{6}(.jpg)", i['file_name']):
                a = i['file_name'].split('.jpg')[0].split('_A')[1]
                i['file_name'] = i['file_name'].split('_A')[0] + '_A' + a[-4:] + '.jpg'
            if re.match("(C)-[0-9]{6}_[0-9]{2}_(CL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('CL')[0] + "CR" + i['file_name'].split('CL')[1]
            if re.match("(C)-[0-9]{6}_[0-9]{2}_(SL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('SL')[0] + "SR" + i['file_name'].split('SL')[1]
            if re.match("(C)-[0-9]{6}_[0-9]{2}_(AL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('AL')[0] + "AR" + i['file_name'].split('AL')[1]
            if re.match("(C)-[0-9]{6}_(08.1)_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('08.1')[0] + "08" + i['file_name'].split('08.1')[1]
            if re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_N[0-9]{4}_[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('_')[0] + '_' + i['file_name'].split('_')[1] + '_' + i['file_name'].split('_')[2] + '_' + i['file_name'].split('_')[3] + '_' + i['file_name'].split('_')[4] + '.jpg'
            if re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_N[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('_N')[0] + "_A" + i['file_name'].split('_N')[1]
            if re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{4}_[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('_')[0] + '_' + i['file_name'].split('_')[1] + '_' + i['file_name'].split('_')[2] + '_' + i['file_name'].split('_')[3] + '_' + i['file_name'].split('_')[4] + '.jpg'
            if re.match("(C)-(229713)_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('229713')[0] + "220713" + i['file_name'].split('229713')[1]
            if re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('_')[0] + '_' + i['file_name'].split('_')[1] + '_' + i['file_name'].split('_')[2] + '_' + i['file_name'].split('_')[3] + '_A' + i['file_name'].split('_')[4]
            if re.match("(C)-[0-9]{6}_[0-9]{2}_(AR07)_(01)_A[0-9]*(.jpg)", i['file_name']):
                i['file_name'] = i['file_name'].split('AR07_01')[0] + 'AR07_03' + i['file_name'].split('AR07_01')[1]


            with open(coco_path, 'w', encoding='UTF-8') as outfile:
                json.dump(coco_json, outfile, indent=4, ensure_ascii=False)


        for i in coco_json['categories']:
            for j in coco_json['annotations']:
                if j['category_id'] == i['id']:
                    if i['name'].startswith('car-06'):
                        if (j['bbox'][2] < 60 and j['bbox'][3] < 100) or (j['bbox'][2] < 100 and j['bbox'][3] < 60):
                            print("좌표범위오류 id, 값 : {}, {}".format(j['image_id']-1, j['bbox']))
                            err_list.loc[num] = [coco_path, j["image_id"]-1, j["bbox"][2], j["bbox"][3]]
                            num += 1
                            j['image_id'] = 0
                            j['category_id'] = 0


                    if not i['name'].startswith('car-06'):
                        if j['bbox'][2] < 150 or j['bbox'][3] < 150 :
                            print("좌표범위오류 id, 값 : {}, {}".format(j['image_id']-1,j['bbox']))
                            err_list.loc[num] = [coco_path, j["image_id"] - 1, j["bbox"][2], j["bbox"][3]]
                            num += 1
                            j['image_id'] = 0
                            j['category_id'] = 0

        d_today = datetime.date.today()
        today = d_today.strftime('%m%d')
        with pd.ExcelWriter("C:/Users/MH46/Desktop/cctv55/err_list/{}_좌표값오류.xlsx".format(today)) as writer:
            err_list.to_excel(writer, sheet_name='좌표값오류', startrow=0, startcol=0)


        with open(coco_path, 'w', encoding='UTF-8') as outfile:
            json.dump(coco_json, outfile, indent=4, ensure_ascii=False)


# jpg 파일명 규칙 검사
def jpg_file_check(file_name):
    check_name = file_name
    if file_name.startswith("Inked"):
        file_check = file_name.split('Inked')[1]
        if not re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{4}(.jpg)", file_check):
            if re.match("(C)-[0-9]{8}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('-20')[0] + '-' + file_check.split('-20')[1]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{6}(.jpg)", file_check):
                a = file_check.split('.jpg')[0].split('_A')[1]
                check_name = file_check.split('_A')[0] + '_A' + a[-4:] + '.jpg'
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('CL')[0] + 'CR' + file_check.split('CL')[1]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(SL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('SL')[0] + 'SR' + file_check.split('SL')[1]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(AL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('AL')[0] + 'AR' + file_check.split('AL')[1]
            elif re.match("(C)-[0-9]{6}_(08.1)_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('08.1')[0] + '08' + file_check.split('08.1')[1]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_N[0-9]{4}_[0-9]*(.jpg)", file_check):
                a = file_check.split('_N')[0] + '_A' + file_check.split('_N')[1]
                check_name = a.split('_')[0] + '_' + a.split('_')[1] + '_' + a.split('_')[2] + '_' + a.split('_')[3] + '_' + a.split('_')[4] + '.jpg'
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_N[0-9]*(.jpg)", file_check):
                check_name = file_check.split('_N')[0] + '_A' + file_check.split('_N')[1]
            elif re.match("(C)-(229713)_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('229713')[0] + "220713" + file_check.split('229713')[1]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{4}_[0-9]*(.jpg)", file_check):
                check_name = file_check.split('_')[0] + '_' + file_check.split('_')[1] + '_' + file_check.split('_')[2] + '_' + file_check.split('_')[3] + '_' + file_check.split('_')[4] + '.jpg'
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_[0-9]*(.jpg)", file_check):
                check_name = file_check.split('_')[0] + '_' + file_check.split('_')[1] + '_' + file_check.split('_')[2] + '_' + file_check.split('_')[3] + '_A' + file_check.split('_')[4]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(AR07)_(01)_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('AR07_01')[0] + 'AR07_03' + file_check.split('AR07_01')[1]
    if file_name.startswith("C-"):
        file_check = file_name
        if not re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{4}(.jpg)", file_check):
            if re.match("(C)-[0-9]{8}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('-20')[0] + '-' + file_check.split('-20')[1]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{6}(.jpg)", file_check):
                a = file_check.split('.jpg')[0].split('_A')[1]
                check_name = file_check.split('_A')[0] + '_A' + a[-4:] + '.jpg'
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('CL')[0] + 'CR' + file_check.split('CL')[1]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(SL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('SL')[0] + 'SR' + file_check.split('SL')[1]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(AL)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('AL')[0] + 'AR' + file_check.split('AL')[1]
            elif re.match("(C)-[0-9]{6}_(08.1)_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('08.1')[0] + '08' + file_check.split('08.1')[1]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_N[0-9]{4}_[0-9]*(.jpg)", file_check):
                a = file_check.split('_N')[0] + '_A' + file_check.split('_N')[1]
                check_name = a.split('_')[0] + '_' + a.split('_')[1] + '_' + a.split('_')[2] + '_' + a.split('_')[3] + '_' + a.split('_')[4] + '.jpg'
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_N[0-9]*(.jpg)", file_check):
                check_name = file_check.split('_N')[0] + '_A' + file_check.split('_N')[1]
            elif re.match("(C)-(229713)_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('229713')[0] + "220713" + file_check.split('229713')[1]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_A[0-9]{4}_[0-9]*(.jpg)", file_check):
                check_name = file_check.split('_')[0] + '_' + file_check.split('_')[1] + '_' + file_check.split('_')[2] + '_' + file_check.split('_')[3] + '_' + file_check.split('_')[4] + '.jpg'
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(CR|SR|AR)[0-9]{2}_[0-9]{2}_[0-9]*(.jpg)", file_check):
                check_name = file_check.split('_')[0] + '_' + file_check.split('_')[1] + '_' + file_check.split('_')[2] + '_' + file_check.split('_')[3] + '_A' + file_check.split('_')[4]
            elif re.match("(C)-[0-9]{6}_[0-9]{2}_(AR07)_(01)_A[0-9]*(.jpg)", file_check):
                check_name = file_check.split('AR07_01')[0] + 'AR07_03' + file_check.split('AR07_01')[1]

    return check_name


# meta 파일 
def json_xlsx():
    path = "C:/Users/MH46/Desktop/cctv55_완료/55_json/"
    meta_xlsx = pd.DataFrame(columns=['구분', '원시 파일명','촬영장소',	'촬영방향', '촬영장소명', '해상도', '촬영일시\n(yyyy-mm-dd)',	'촬영 시작 시간',	'촬영 종료 시간',	'영상길이(초) [고정]',	'FPS\n[고정]', '계절',
                          '날씨', '평일/주말/휴일', '도로 유형', '교차로 유형', 'CCTV 카메라 유형',	'CCTV 렌즈\n유형', 'CCTV 설치높이', 'CCTV 각도', 'CCTV GPS정보', '추출시간\n(hh:mm:ss)', '파일명', 'task'])
    meta_xlsx = meta_xlsx.set_index('구분')
    a = 1


    for path_name in os.listdir(path):
        with open(path+'/'+path_name, 'r', encoding='UTF-8') as json_file:
            coco_json = json.load(json_file)

        meta_xlsx.loc[a] = [coco_json['Raw Data Info']['raw_data_id'], coco_json['Raw Data Info']['location_id'], coco_json['Raw Data Info']['cctv_number'], coco_json['Raw Data Info']['location_name'],
                            [1920, 1080], coco_json['Raw Data Info']['date'], coco_json['Raw Data Info']['start_time'], coco_json['Raw Data Info']['end_time'], 3600, 30,
                            coco_json['Raw Data Info']['season'], coco_json['Raw Data Info']['weather'], coco_json['Raw Data Info']['day_type'], coco_json['Raw Data Info']['road_type'],
                            coco_json['Raw Data Info']['cross_type'], coco_json['Raw Data Info']['cctv_type'], coco_json['Raw Data Info']['lens_type'], coco_json['Raw Data Info']['cctv_height'],
                            coco_json['Raw Data Info']['cctv_angle'], coco_json['Raw Data Info']['cctv_gps'], coco_json['Source Data Info']['extract_time'], coco_json['Source Data Info']['source_data_id'], 0]
        a += 1
        print(a)

    task_path = 'C:/Users/MH46/Desktop/cctv55/inspection_json'
    task_name = []

    for i in os.listdir(task_path):
        task_name = i.split('.')[0]
        with open(task_path + '/' + i, 'r', encoding='UTF-8') as json_file:
            coco_json = json.load(json_file)
        for index, row in meta_xlsx.iterrows():
            for json_name in coco_json['images']:
                if row['파일명'] == json_name['file_name'].split('.')[0]:
                    meta_xlsx.loc[index, 'task'] = task_name
                    print(task_name)

    d_today = datetime.date.today()
    today = d_today.strftime('%m%d')
    filename = "meta_{}.xlsx".format(today)
    end_path = "C:/Users/MH46/Desktop/완료_meta/{}".format(filename)

    with pd.ExcelWriter(end_path) as writer:
        meta_xlsx.to_excel(writer, sheet_name='메타', startrow=0 ,startcol=0)

# 완성데이터 대기 
def file_move():
    path = ""
    nas_path = "\\\\192.168."
    nas_jpg_path = "\\\\192.168."
    jpg_path = ""
    end_json = ""
    end_jpg = ""
    learn_json_copy = "\\\\192.168."
    learn_jpg_copy = "\\\\192.168."
    a = []
    for jpg_path_name in os.listdir(jpg_path):
        a.append(jpg_path_name.split('.')[0])
    num = 1

    for path_name in os.listdir(path):
        if path_name.split('.')[0] in a:
            with open(path + '/' + path_name, 'r', encoding='UTF-8') as json_file:
                coco_json = json.load(json_file)

            nas_path2 = coco_json['Learning Data Info']['path'].split('/')[2] + "\\" + coco_json['Learning Data Info']['path'].split('/')[3] + '\\' + coco_json['Learning Data Info']['path'].split('/')[4] + "\\" + coco_json['Source Data Info']['source_data_id']
            shutil.copy(path + path_name, nas_path + nas_path2 + '.json')
            shutil.copy(path + path_name, learn_json_copy + path_name.split('.')[0] + '.json')
            shutil.move(path + path_name, end_json + path_name.split('.')[0] + '.json')

            shutil.copy(jpg_path + path_name.split('.')[0] + '.jpg', nas_jpg_path + nas_path2 + '.jpg')
            shutil.copy(jpg_path + path_name.split('.')[0] + '.jpg', learn_jpg_copy + path_name.split('.')[0] + '.jpg')
            shutil.move(jpg_path + path_name.split('.')[0] + '.jpg', end_jpg + path_name.split('.')[0] + '.jpg')

            print("완료 : {} {}".format(num, path_name))
            num += 1

            
# 완성데이터 
def end_file_move():
    jpg_path = ""
    path = ""
    nas_path = ""
    nas_jpg_path = ""

    a = []
    for jpg_path_name in os.listdir(jpg_path):
        a.append(jpg_path_name.split('.')[0])
    num = 1

    for path_name in os.listdir(path):
        if path_name.split('.')[0] in a:
            with open(path + '/' + path_name, 'r', encoding='UTF-8') as json_file:
                coco_json = json.load(json_file)

            nas_path2 = coco_json['Learning Data Info']['path'].split('/')[1] + "\\" + \
                        coco_json['Learning Data Info']['path'].split('/')[2] + "\\" + \
                        coco_json['Learning Data Info']['path'].split('/')[3] + "\\" + \
                        coco_json['Learning Data Info']['path'].split('/')[4] + "\\" + coco_json['Source Data Info'][
                            'source_data_id']
            shutil.move(path + path_name, nas_path + nas_path2 + '.json')

            shutil.move(jpg_path + path_name.split('.')[0] + '.jpg', nas_jpg_path + nas_path2 + '.jpg')

            print("완료 : {} {}".format(num, path_name))
            num += 1




# coco_file_check() : json 생성 전 파일명 규칙 및 픽셀 검사
# json_xlsx() : Meta 생성
# file_move() : NAS 에 파일 이동 및 복사
# end_file_move() : 완성데이터에 업로드 마친 파일 D드라이브에 이동
#
# print(json_xlsx())




# # 특정 차종 검색
# path = "D:/완성데이터/라벨링데이터/차종외관인식/"
# jpg_path = "D:/완성데이터/원천데이터/차종외관인식/"
# check_task = pd.read_excel("C:/Users/MH46/Desktop/전수검사task.xlsx")
# check_path = "C:/Users/MH46/Desktop/전수검사완료/완성대기/"
# car01 = pd.DataFrame(columns=['task', 'file_name', 'class_id', 'brand_id', 'model_id'])
# car02 = pd.DataFrame(columns=['task', 'file_name', 'class_id', 'brand_id', 'model_id'])
# car03 = pd.DataFrame(columns=['task', 'file_name', 'class_id', 'brand_id', 'model_id'])
# car04 = pd.DataFrame(columns=['task', 'file_name', 'class_id', 'brand_id', 'model_id'])
# car05 = pd.DataFrame(columns=['task', 'file_name', 'class_id', 'brand_id', 'model_id'])
# car07 = pd.DataFrame(columns=['task', 'file_name', 'class_id', 'brand_id', 'model_id'])
#
# num = 1
# check_list = []
# check_task_list = []
#
# for i in os.listdir(check_path):
#     check_list.append(i)
# for i in check_task['task']:
#     check_task_list.append(i)
#
# for (root, directory, files) in os.walk(path):
#     if root.endswith('번'):
#         print(root)
#         for i in os.listdir(root):
#             task = i.split('_')[0] + i.split('_')[2] + i.split('_')[3]
#             if i not in check_list:
#                 if task not in check_task['task']:
#                     print(i)
#
#                     with open(root + '\\' + i, 'r', encoding='UTF-8') as json_file:
#                         coco_json = json.load(json_file)
#
#                     for j in coco_json["Learning Data Info"]["annotations"]:
#
#                         if (j['model_id'] == "스타렉스_그랜드 더뉴(2017)") or (j['model_id'] == "스타렉스_그랜드(2007)") or (j['model_id'] == "스타렉스_스타렉스(1997)"):
#                             car01.loc[num, 'task'] = task
#                             car01.loc[num, 'file_name'] = i
#                             car01.loc[num, 'class_id'] = j['class_id']
#                             car01.loc[num, 'brand_id'] = j['brand_id']
#                             car01.loc[num, 'model_id'] = j['model_id']
#
#
#                             nas_path2 = coco_json['Learning Data Info']['path'].split('/')[2] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[3] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[4] + "\\" + \
#                                         coco_json['Source Data Info'][
#                                             'source_data_id']
#                             shutil.copy(root + '/' + i, "D:/json 수정파일/전수검사제외_unknown/car-01/라벨링데이터/" + i)
#                             shutil.copy(jpg_path + nas_path2 + '.jpg', "D:/json 수정파일/전수검사제외_unknown/car-01/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             print("D:/json 수정파일/전수검사제외_unknown/car-01/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             num += 1
#
#                         if (j['class_id'] == "car-02") and (j['brand_id'] == "Unknown") and (j['model_id'] == "Unknown"):
#                             car02.loc[num, 'task'] = task
#                             car02.loc[num, 'file_name'] = i
#                             car02.loc[num, 'class_id'] = j['class_id']
#                             car02.loc[num, 'brand_id'] = j['brand_id']
#                             car02.loc[num, 'model_id'] = j['model_id']
#
#
#                             nas_path2 = coco_json['Learning Data Info']['path'].split('/')[2] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[3] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[4] + "\\" + \
#                                         coco_json['Source Data Info'][
#                                             'source_data_id']
#                             shutil.copy(root + '/' + i, "D:/json 수정파일/전수검사제외_unknown/car-02/라벨링데이터/" + i)
#                             shutil.copy(jpg_path + nas_path2 + '.jpg', "D:/json 수정파일/전수검사제외_unknown/car-02/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             print("D:/json 수정파일/전수검사제외_unknown/car-02/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             num += 1
#
#                         if (j['class_id'] == "car-03") and (j['brand_id'] == "Unknown") and (j['model_id'] == "Unknown"):
#                             car03.loc[num, 'task'] = task
#                             car03.loc[num, 'file_name'] = i
#                             car03.loc[num, 'class_id'] = j['class_id']
#                             car03.loc[num, 'brand_id'] = j['brand_id']
#                             car03.loc[num, 'model_id'] = j['model_id']
#
#
#                             nas_path2 = coco_json['Learning Data Info']['path'].split('/')[2] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[3] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[4] + "\\" + \
#                                         coco_json['Source Data Info'][
#                                             'source_data_id']
#                             shutil.copy(root + '/' + i, "D:/json 수정파일/전수검사제외_unknown/car-03/라벨링데이터/" + i)
#                             shutil.copy(jpg_path + nas_path2 + '.jpg', "D:/json 수정파일/전수검사제외_unknown/car-03/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             print("D:/json 수정파일/전수검사제외_unknown/car-03/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             num += 1
#
#
#                         if (j['class_id'] == "car-04") and (j['brand_id'] == "Unknown") and (j['model_id'] == "Unknown"):
#                             car04.loc[num, 'task'] = task
#                             car04.loc[num, 'file_name'] = i
#                             car04.loc[num, 'class_id'] = j['class_id']
#                             car04.loc[num, 'brand_id'] = j['brand_id']
#                             car04.loc[num, 'model_id'] = j['model_id']
#
#
#                             nas_path2 = coco_json['Learning Data Info']['path'].split('/')[2] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[3] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[4] + "\\" + \
#                                         coco_json['Source Data Info'][
#                                             'source_data_id']
#                             shutil.copy(root + '/' + i, "D:/json 수정파일/전수검사제외_unknown/car-04/라벨링데이터/" + i)
#                             shutil.copy(jpg_path + nas_path2 + '.jpg', "D:/json 수정파일/전수검사제외_unknown/car-04/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             print("D:/json 수정파일/전수검사제외_unknown/car-04/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             num += 1
#
#                         if (j['class_id'] == "car-05") and (j['brand_id'] == "Unknown") and (j['model_id'] == "Unknown"):
#                             car05.loc[num, 'task'] = task
#                             car05.loc[num, 'file_name'] = i
#                             car05.loc[num, 'class_id'] = j['class_id']
#                             car05.loc[num, 'brand_id'] = j['brand_id']
#                             car05.loc[num, 'model_id'] = j['model_id']
#
#
#                             nas_path2 = coco_json['Learning Data Info']['path'].split('/')[2] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[3] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[4] + "\\" + \
#                                         coco_json['Source Data Info'][
#                                             'source_data_id']
#                             shutil.copy(root + '/' + i, "D:/json 수정파일/전수검사제외_unknown/car-05/라벨링데이터/" + i)
#                             shutil.copy(jpg_path + nas_path2 + '.jpg', "D:/json 수정파일/전수검사제외_unknown/car-05/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             print("D:/json 수정파일/전수검사제외_unknown/car-05/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             num += 1
#
#                         if (j['class_id'] == "car-07") and (j['brand_id'] == "Unknown") and (j['model_id'] == "Unknown"):
#                             car07.loc[num, 'task'] = task
#                             car07.loc[num, 'file_name'] = i
#                             car07.loc[num, 'class_id'] = j['class_id']
#                             car07.loc[num, 'brand_id'] = j['brand_id']
#                             car07.loc[num, 'model_id'] = j['model_id']
#
#
#                             nas_path2 = coco_json['Learning Data Info']['path'].split('/')[2] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[3] + "\\" + \
#                                         coco_json['Learning Data Info']['path'].split('/')[4] + "\\" + \
#                                         coco_json['Source Data Info'][
#                                             'source_data_id']
#                             shutil.copy(root + '/' + i, "D:/json 수정파일/전수검사제외_unknown/car-07/라벨링데이터/" + i)
#                             shutil.copy(jpg_path + nas_path2 + '.jpg', "D:/json 수정파일/전수검사제외_unknown/car-07/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             print("D:/json 수정파일/전수검사제외_unknown/car-07/원천데이터/" + coco_json['Source Data Info'][
#                                             'source_data_id'] + '.jpg')
#                             num += 1
#
# with pd.ExcelWriter('D:/json 수정파일/전수검사제외_unknown/전수검사제외_unknown.xlsx') as writer:
#     car01.to_excel(writer, sheet_name='car-01', startrow=0 ,startcol=0)
#     car02.to_excel(writer, sheet_name='car-02', startrow=0 ,startcol=0)
#     car03.to_excel(writer, sheet_name='car-03', startrow=0 ,startcol=0)
#     car04.to_excel(writer, sheet_name='car-04', startrow=0 ,startcol=0)
#     car05.to_excel(writer, sheet_name='car-05', startrow=0 ,startcol=0)
#     car07.to_excel(writer, sheet_name='car-07', startrow=0 ,startcol=0)
#
