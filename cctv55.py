# path 등 변수는 상황에 맞춰 수정하여 사용하였으니 코드 실행 전 확인 할 것


import json
import pandas as pd
import os
import datetime
import shutil
import re
import random



def coco_file_check():
    # coco json 불러오기
    ins_path = 'C:/Users/MH46/Desktop/cctv55/inspection_json'
    int_path = 'C:/Users/MH46/Desktop/완성json_대기/55_json'
    jpg_path = 'C:/Users/MH46/Desktop/cctv55/jpg/'
    # jpg_path = 'C:/Users/MH46/Desktop/완성json_대기/jpg/'
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


def file_move():
    path = "C:/Users/MH46/Desktop/완성json_대기/55_json/"
    # path = "D:/이동완료/55_json/"
    nas_path = "\\\\192.168.0.150\\완성데이터\\라벨링데이터\\차종외관인식\\"
    nas_jpg_path = "\\\\192.168.0.150\\완성데이터\\원천데이터\\차종외관인식\\"
    # nas_move_path = "\\\\192.168.0.150\\원천데이터\\차종외관\\"
    # jpg_path = "E:/55_cctv/nas_jpg/"
    # jpg_path = "D:/이동완료/55_jpg/"
    jpg_path = "C:/Users/MH46/Desktop/완성json_대기/jpg/"
    end_json = "C:/Users/MH46/Desktop/완성json_대기/이동완료/55_json/"
    # end_jpg = "E:/55_cctv/완료_nas_jpg/"
    end_jpg = "C:/Users/MH46/Desktop/완성json_대기/이동완료/55_jpg/"
    run_json_copy = "\\\\192.168.0.150\\학습용데이터\\차종외관\\12월3주차\\라벨링데이터\\"
    run_jpg_copy = "\\\\192.168.0.150\\학습용데이터\\차종외관\\12월3주차\\원천데이터\\"
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
            shutil.copy(path + path_name, run_json_copy + path_name.split('.')[0] + '.json')
            shutil.move(path + path_name, end_json + path_name.split('.')[0] + '.json')

            shutil.copy(jpg_path + path_name.split('.')[0] + '.jpg', nas_jpg_path + nas_path2 + '.jpg')
            shutil.copy(jpg_path + path_name.split('.')[0] + '.jpg', run_jpg_copy + path_name.split('.')[0] + '.jpg')
            shutil.move(jpg_path + path_name.split('.')[0] + '.jpg', end_jpg + path_name.split('.')[0] + '.jpg')

            print("완료 : {} {}".format(num, path_name))
            num += 1

def end_file_move():
    jpg_path = "C:/Users/MH46/Desktop/완성json_대기/이동완료/55_jpg/"
    path = "C:/Users/MH46/Desktop/완성json_대기/이동완료/55_json/"
    nas_path = "D:/완성데이터/라벨링데이터/"
    nas_jpg_path = "D:/완성데이터/원천데이터/"

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

# # 시간 데이터 수정
# path = 'D:/완성데이터/라벨링데이터/차종외관인식/'
# road_check = pd.read_excel("C:/Users/MH46/Desktop/cctv55/55_Meta_check.xlsx", sheet_name='path')
# file09 = pd.DataFrame(columns=['file'])
# file09_new = pd.DataFrame(columns=['file'])
# file10 = pd.DataFrame(columns=['file'])
# file10_new = pd.DataFrame(columns=['file'])
# file10_2 = pd.DataFrame(columns=['file'])
# file10_new_2 = pd.DataFrame(columns=['file'])
# file11_1 = pd.DataFrame(columns=['file'])
# file11_new_1 = pd.DataFrame(columns=['file'])
# file11_2 = pd.DataFrame(columns=['file'])
# file11_new_2 = pd.DataFrame(columns=['file'])
# file12 = pd.DataFrame(columns=['file'])
# file12_new = pd.DataFrame(columns=['file'])
# file13_15 = pd.DataFrame(columns=['file'])
# file13_15_new = pd.DataFrame(columns=['file'])
# file16 = pd.DataFrame(columns=['file'])
# file16_new = pd.DataFrame(columns=['file'])
# err = pd.DataFrame(columns=['file'])
# err_num = 1
# num = 1
#
# time09to08 = 10000
# time10to08 = 45000
# time11_15 = 15000
#
# num09_check = 1
# num10_check1 = 1
# num10_check2 = 1
# num11_check1 = 1
# num11_check2 = 1
# num12_check = 1
# num13_check = 1
# num14_check = 1
# num15_check = 1
# num16_check = 1
#
# for index, row in road_check.iterrows():
#     print("{} 데이터 변경 시작".format(row['촬영장소']))
#     for root, directory, files in os.walk(path):
#         if root.endswith('번'):
#             num09 = 5000
#
#             for file in os.listdir(root):
#                 time = file.split('_')[1]
#                 road = file.split('_')[2]
#                 a = file.split('.')[0]
#                 aa = a.split('_')[4]
#                 file_num = aa.split('A')[1]
#
#                 if file_num < "5000":
#                     # 9시를 8시로 타임 변경 시작
#                     if time == '09':
#                         if (road.lower() == row['촬영장소']) and (num09_check <= time09to08):
#                             print("시간변경중 : {}".format(file))
#                             json_path = root + '/' + file
#                             file_name = file.split('.')[0]
#
#                             with open(json_path, 'r', encoding='UTF-8') as json_file:
#                                 coco_json = json.load(json_file)
#                             ex_time = coco_json["Source Data Info"]["extract_time"]
#
#                             file09.loc[num, 'file'] = file
#                             file09.loc[num, 'raw_data_id'] = coco_json["Raw Data Info"]["raw_data_id"]
#                             file09.loc[num, 'start_time'] = coco_json["Raw Data Info"]["start_time"]
#                             file09.loc[num, 'end_time'] = coco_json["Raw Data Info"]["end_time"]
#                             file09.loc[num, 'source_data_id'] = coco_json["Source Data Info"]["source_data_id"]
#                             file09.loc[num, 'json_data_id'] = coco_json["Learning Data Info"]["json_data_id"]
#
#                             coco_json["Raw Data Info"]["raw_data_id"] = file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3]
#                             coco_json["Raw Data Info"]["start_time"] = "08:00:00"
#                             coco_json["Raw Data Info"]["end_time"] = "09:00:00"
#                             coco_json["Source Data Info"]["source_data_id"] = file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num09)
#                             coco_json["Source Data Info"]["extract_time"] = "{}:{}:{}".format('08', ex_time.split(':')[1], ex_time.split(':')[2])
#                             coco_json["Learning Data Info"]["json_data_id"] = file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num09)
#
#                             file09_new.loc[num, 'file'] = file
#                             file09_new.loc[num, 'new_file'] = file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num09)
#                             file09_new.loc[num, 'new_raw_data_id'] = coco_json["Raw Data Info"]["raw_data_id"]
#                             file09_new.loc[num, 'new_start_time'] = coco_json["Raw Data Info"]["start_time"]
#                             file09_new.loc[num, 'new_end_time'] = coco_json["Raw Data Info"]["end_time"]
#                             file09_new.loc[num, 'new_source_data_id'] = coco_json["Source Data Info"]["source_data_id"]
#                             file09_new.loc[num, 'new_json_data_id'] = coco_json["Learning Data Info"]["json_data_id"]
#
#                             with open(json_path, 'w', encoding='UTF-8') as outfile:
#                                 json.dump(coco_json, outfile, indent=4, ensure_ascii=False)
#                             jpg_path = 'D:/완성데이터/원천데이터/' + coco_json["Learning Data Info"]["path"] + '/'
#                             if os.path.exists(root + '/' + file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num09) + '.json'):
#                                 err.loc[err_num, file] = file
#                                 err_num += 1
#                             if not os.path.exists(
#                                     root + '/' + file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[
#                                         3] + '_A' + str(num09) + '.json'):
#                                 os.rename(json_path, root + '/' + file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num09) + '.json')
#                                 os.rename(jpg_path + file_name + '.jpg', jpg_path + file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num09) + '.jpg')
#
#                             num09_check += 1
#                             num09 += 1
#                             num += 1
# with pd.ExcelWriter("C:/Users/MH46/Desktop/시간데이터수정/file09.xlsx") as writer:
#     file09.to_excel(writer, sheet_name='원본', startrow=0, startcol=0)
#     file09_new.to_excel(writer, sheet_name='변경', startrow=0, startcol=0)
#
#
#
# for index, row in road_check.iterrows():
#     print("{} 데이터 변경 시작".format(row['촬영장소']))
#     for root, directory, files in os.walk(path):
#         if root.endswith('번'):
#             num10_1 = 5000
#             num10_2 = 5000
#
#             for file in os.listdir(root):
#                 time = file.split('_')[1]
#                 road = file.split('_')[2]
#                 a = file.split('.')[0]
#                 aa = a.split('_')[4]
#                 file_num = aa.split('A')[1]
#
#                 if file_num < "5000":
#                     # 10시를 타임 08 time 변경 시작
#                     if time == '10':
#                         if (road.lower() == row['촬영장소']) and (num10_check1 <= time10to08):
#
#                             print("시간변경중 : {}".format(file))
#                             json_path = root + '/' + file
#                             file_name = file.split('.')[0]
#
#                             with open(json_path, 'r', encoding='UTF-8') as json_file:
#                                 coco_json = json.load(json_file)
#                             ex_time = coco_json["Source Data Info"]["extract_time"]
#
#                             file10.loc[num, 'file'] = file
#                             file10.loc[num, 'raw_data_id'] = coco_json["Raw Data Info"]["raw_data_id"]
#                             file10.loc[num, 'start_time'] = coco_json["Raw Data Info"]["start_time"]
#                             file10.loc[num, 'end_time'] = coco_json["Raw Data Info"]["end_time"]
#                             file10.loc[num, 'source_data_id'] = coco_json["Source Data Info"]["source_data_id"]
#                             file10.loc[num, 'json_data_id'] = coco_json["Learning Data Info"]["json_data_id"]
#
#                             coco_json["Raw Data Info"]["raw_data_id"] = file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3]
#                             coco_json["Raw Data Info"]["start_time"] = "08:00:00"
#                             coco_json["Raw Data Info"]["end_time"] = "09:00:00"
#                             coco_json["Source Data Info"]["source_data_id"] = file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num10_1)
#                             coco_json["Source Data Info"]["extract_time"] = "{}:{}:{}".format('08', ex_time.split(':')[1], ex_time.split(':')[2])
#                             coco_json["Learning Data Info"]["json_data_id"] = file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num10_1)
#
#                             file10_new.loc[num, 'file'] = file
#                             file10_new.loc[num, 'new_file'] = file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num10_1)
#                             file10_new.loc[num, 'new_raw_data_id'] = coco_json["Raw Data Info"]["raw_data_id"]
#                             file10_new.loc[num, 'new_start_time'] = coco_json["Raw Data Info"]["start_time"]
#                             file10_new.loc[num, 'new_end_time'] = coco_json["Raw Data Info"]["end_time"]
#                             file10_new.loc[num, 'new_source_data_id'] = coco_json["Source Data Info"]["source_data_id"]
#                             file10_new.loc[num, 'new_json_data_id'] = coco_json["Learning Data Info"]["json_data_id"]
#
#                             with open(json_path, 'w', encoding='UTF-8') as outfile:
#                                 json.dump(coco_json, outfile, indent=4, ensure_ascii=False)
#                             jpg_path = 'D:/완성데이터/원천데이터/' + coco_json["Learning Data Info"]["path"] + '/'
#                             if os.path.exists(root + '/' + file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num10_1) + '.json'):
#                                 err.loc[err_num, file] = file
#                                 err_num += 1
#                             if not os.path.exists(root + '/' + file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num10_1) + '.json'):
#                                 os.rename(json_path, root + '/' + file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num10_1) + '.json')
#                                 os.rename(jpg_path + file_name + '.jpg', jpg_path + file.split('_')[0] + '_08_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num10_1) + '.jpg')
#
#                             num10_check1 += 1
#                             num10_1 += 1
#                             num += 1
#
# with pd.ExcelWriter("C:/Users/MH46/Desktop/시간데이터수정/file10.xlsx") as writer:
#     file10.to_excel(writer, sheet_name='원본', startrow=0, startcol=0)
#     file10_new.to_excel(writer, sheet_name='변경', startrow=0, startcol=0)
#
#
# for index, row in road_check.iterrows():
#     print("{} 데이터 변경 시작".format(row['촬영장소']))
#     for root, directory, files in os.walk(path):
#         if root.endswith('번'):
#             num11_1 = 5000
#             num11_2 = 5000
#
#             for file in os.listdir(root):
#                 time = file.split('_')[1]
#                 road = file.split('_')[2]
#                 a = file.split('.')[0]
#                 aa = a.split('_')[4]
#                 file_num = aa.split('A')[1]
#
#                 if file_num < "5000":
#
#                     if time == '11':
#
#                         # 11 to 12
#                         if (road.lower() == row['촬영장소']) and (num11_check2 <= time11_15):
#
#                             print("시간변경중 : {}".format(file))
#                             json_path = root + '/' + file
#                             file_name = file.split('.')[0]
#
#                             with open(json_path, 'r', encoding='UTF-8') as json_file:
#                                 coco_json = json.load(json_file)
#                             ex_time = coco_json["Source Data Info"]["extract_time"]
#
#                             file11_2.loc[num, 'file'] = file
#                             file11_2.loc[num, 'raw_data_id'] = coco_json["Raw Data Info"]["raw_data_id"]
#                             file11_2.loc[num, 'start_time'] = coco_json["Raw Data Info"]["start_time"]
#                             file11_2.loc[num, 'end_time'] = coco_json["Raw Data Info"]["end_time"]
#                             file11_2.loc[num, 'source_data_id'] = coco_json["Source Data Info"]["source_data_id"]
#                             file11_2.loc[num, 'json_data_id'] = coco_json["Learning Data Info"]["json_data_id"]
#
#                             coco_json["Raw Data Info"]["raw_data_id"] = file.split('_')[0] + '_12_' + file.split('_')[
#                                 2] + '_' + file.split('_')[3]
#                             coco_json["Raw Data Info"]["start_time"] = "12:00:00"
#                             coco_json["Raw Data Info"]["end_time"] = "13:00:00"
#                             coco_json["Source Data Info"]["source_data_id"] = file.split('_')[0] + '_12_' + file.split('_')[
#                                 2] + '_' + file.split('_')[3] + '_A' + str(num11_2)
#                             coco_json["Source Data Info"]["extract_time"] = "{}:{}:{}".format('12', ex_time.split(':')[1],
#                                                                                               ex_time.split(':')[2])
#                             coco_json["Learning Data Info"]["json_data_id"] = file.split('_')[0] + '_12_' + file.split('_')[
#                                 2] + '_' + file.split('_')[3] + '_A' + str(num11_2)
#
#                             file11_new_2.loc[num, 'file'] = file
#                             file11_new_2.loc[num, 'new_file'] = file.split('_')[0] + '_12_' + file.split('_')[2] + '_' + \
#                                                                 file.split('_')[3] + '_A' + str(num11_2)
#                             file11_new_2.loc[num, 'new_raw_data_id'] = coco_json["Raw Data Info"]["raw_data_id"]
#                             file11_new_2.loc[num, 'new_start_time'] = coco_json["Raw Data Info"]["start_time"]
#                             file11_new_2.loc[num, 'new_end_time'] = coco_json["Raw Data Info"]["end_time"]
#                             file11_new_2.loc[num, 'new_source_data_id'] = coco_json["Source Data Info"]["source_data_id"]
#                             file11_new_2.loc[num, 'new_json_data_id'] = coco_json["Learning Data Info"]["json_data_id"]
#
#                             with open(json_path, 'w', encoding='UTF-8') as outfile:
#                                 json.dump(coco_json, outfile, indent=4, ensure_ascii=False)
#                             jpg_path = 'D:/완성데이터/원천데이터/' + coco_json["Learning Data Info"]["path"] + '/'
#
#                             if os.path.exists(root + '/' + file.split('_')[0] + '_12_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num11_2) + '.json'):
#                                 err.loc[err_num, file] = file
#                                 err_num += 1
#                             if not os.path.exists(root + '/' + file.split('_')[0] + '_12_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num11_2) + '.json'):
#                                 os.rename(json_path, root + '/' + file.split('_')[0] + '_12_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num11_2) + '.json')
#                                 os.rename(jpg_path + file_name + '.jpg', jpg_path + file.split('_')[0] + '_12_' + file.split('_')[2] + '_' + file.split('_')[3] + '_A' + str(num11_2) + '.jpg')
#
#                             num11_check2 += 1
#                             num11_2 += 1
#                             num += 1
# with pd.ExcelWriter("C:/Users/MH46/Desktop/시간데이터수정/file11_2.xlsx") as writer:
#     file11_2.to_excel(writer, sheet_name='원본', startrow=0, startcol=0)
#     file11_new_2.to_excel(writer, sheet_name='변경', startrow=0, startcol=0)
#



# # 파일 개수 검사
# json_path = "D:/완성데이터/라벨링데이터/차종외관인식/"
# jpg_path = "D:/완성데이터/원천데이터/차종외관인식/"
# path_xlsx = pd.DataFrame(columns=['라벨링경로', '라벨링개수', '이미지경로', '이미지개수'])
# num = 1
#
# for (root, directory, files) in os.walk(json_path):
#     if root.endswith('번'):
#         path_xlsx.loc[num, '라벨링경로'] = root
#         path_xlsx.loc[num, '라벨링개수'] = len(os.listdir(root))
#         num += 1
#
# num = 1
#
# for (root, directory, files) in os.walk(jpg_path):
#     if root.endswith('번'):
#         path_xlsx.loc[num, '이미지경로'] = root
#         path_xlsx.loc[num, '이미지개수'] = len(os.listdir(root))
#         num += 1
#
#
# with pd.ExcelWriter("C:/Users/MH46/Desktop/파일개수.xlsx") as writer:
#     path_xlsx.to_excel(writer, sheet_name='개수')
#





# #
# #
# # # 비오는 날 수정
# # change_weather = pd.read_excel("C:/Users/MH46/Desktop/weather.xlsx", sheet_name='Sheet2')
# #
# # for index, row in change_weather.iterrows():
# #     json_path = 'D:/완성데이터/라벨링데이터/차종외관인식/{}/{}/{}/{}'.format(row['도로'], row['도로명'], row['카메라'], row['파일명'])
# #     if os.path.exists(json_path):
# #         with open(json_path, 'r', encoding='UTF-8') as json_file:
# #             coco_json = json.load(json_file)
# #
# #         coco_json["Raw Data Info"]["weather"] = row['weather']
# #
# #         with open(json_path, 'w', encoding='UTF-8') as outfile:
# #             json.dump(coco_json, outfile, indent=4, ensure_ascii=False)



# # 비오는 시간대 s 집계
# path = 'D:/완성데이터/라벨링데이터/차종외관인식'
#
# import json
# import os
# import pandas as pd
#
# json_path_list = []
# for i in os.listdir(path):
#     for j in os.listdir(path + '/' + i):
#         for m in os.listdir(path + '/' + i + '/' + j):
#             json_path_list.append(path + '/' + i + '/' + j + '/' + m)
#
# # rain_time_df  = pd.DataFrame(columns = ['구분','도로''도로명','카메라','시간'])
# rain_time_list = []
#
# for i in json_path_list[:]:
#     jpath = os.listdir(i)
#     for j in jpath[:]:
#         rain_time = i.split('/')[-2] + '/' + i.split('/')[-1] + '/' + j[2:8] + '/' + j.split('_')[1] + '시'
#         if rain_time not in rain_time_list:
#             print(j)
#             with open(i + '/' + j, 'r', encoding='UTF8') as file:
#                 json_data = json.load(file)
#             if json_data['Raw Data Info']['weather'] == 'r':
#                 if rain_time not in rain_time_list:
#                     rain_time_list.append(rain_time)
#
# new_df = pd.DataFrame(columns=['구분', '도로', '도로명', '카메라', '파일명', 'date', 'extract_time', 'weather'])
# aa = 0
# bb = 0
# a = 0
# for i in json_path_list[:]:
#     jpath = os.listdir(i)
#     # location_weather = rain_time_df[rain_time_df['location']==i.split[-2]]
#     for j in jpath[:]:
#         if i.split('/')[-2] + '/' + i.split('/')[-1] + '/' + j[2:8] + '/' + j.split('_')[1] + '시' in rain_time_list:
#             aa += 1
#             if 'cr' in i:
#                 road = '교차로'
#             elif 'sr' in i:
#                 road = '이면도로'
#             elif 'ar' in i:
#                 road = '접근로'
#
#             with open(i + '/' + j, 'r', encoding='UTF8') as file:
#                 json_data = json.load(file)
#             if json_data['Raw Data Info']['weather'] == 's':
#                 a += 1
#                 new_df.loc[a, "구분"] = a
#                 new_df.loc[a, "도로"] = road
#                 new_df.loc[a, "도로명"] = i.split('/')[-2]
#                 new_df.loc[a, "카메라"] = json_data["Raw Data Info"]["cctv_number"] + '번'
#                 new_df.loc[a, "파일명"] = j
#                 new_df.loc[a, "date"] = json_data["Raw Data Info"]["date"]
#                 new_df.loc[a, "extract_time"] = json_data["Source Data Info"]["extract_time"]
#                 new_df.loc[a, "weather"] = json_data["Raw Data Info"]["weather"]
#                 bb += 1
#
# print('비오는 시간 개수 : ' + str(aa))
# print('비오는 시간 중 s 개수 : ' + str(bb))
#
# with pd.ExcelWriter('C:/Users/MH46/Desktop/weather_time.xlsx') as writer:
#     new_df.to_excel(writer, index=False)

#
# # 날씨 확인
#
# path = 'D:/완성데이터/라벨링데이터/차종외관인식/'
# xlsx_a = "C:/Users/MH46/Desktop/날씨에러.xlsx"
# s = 0
# f = 0
# r = 0
# etc = pd.DataFrame(columns=['root', 'file'])
# time = pd.read_excel(xlsx_a, sheet_name='시간통계', index_col=1)
# num = 1
# time['1222'] = 0
#
# for root, directory, files in os.walk(path):
#     if root.endswith('번'):
#         print("검색중 : {}".format(root))
#         for i in os.listdir(root):
#             with open(root + '\\' + i, 'r', encoding='UTF-8') as json_file:
#                 coco_json = json.load(json_file)
#
#                 if coco_json["Raw Data Info"]["weather"] == "s":
#                     s += 1
#                 if coco_json["Raw Data Info"]["weather"] == "f":
#                     f += 1
#                 if coco_json["Raw Data Info"]["weather"] == "r":
#                     r += 1
#
#                 print(i)
#
#                 if coco_json["Raw Data Info"]["start_time"] == "00:00:00":
#                     time.loc["00:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "01:00:00":
#                     time.loc["01:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "02:00:00":
#                     time.loc["02:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "03:00:00":
#                     time.loc["03:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "04:00:00":
#                     time.loc["04:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "05:00:00":
#                     time.loc["05:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "06:00:00":
#                     time.loc["06:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "07:00:00":
#                     time.loc["07:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "08:00:00":
#                     time.loc["08:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "09:00:00":
#                     time.loc["09:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "10:00:00":
#                     time.loc["10:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "11:00:00":
#                     time.loc["11:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "12:00:00":
#                     time.loc["12:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "13:00:00":
#                     time.loc["13:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "14:00:00":
#                     time.loc["14:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "15:00:00":
#                     time.loc["15:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "16:00:00":
#                     time.loc["16:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "17:00:00":
#                     time.loc["17:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "18:00:00":
#                     time.loc["18:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "19:00:00":
#                     time.loc["19:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "20:00:00":
#                     time.loc["20:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "21:00:00":
#                     time.loc["21:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "22:00:00":
#                     time.loc["22:00:00", '1222'] += 1
#                 elif coco_json["Raw Data Info"]["start_time"] == "23:00:00":
#                     time.loc["23:00:00", '1222'] += 1
#
#                 print(i)
#
# print("s : {}".format(s))
# print("f : {}".format(f))
# print("r : {}".format(r))
#
# with pd.ExcelWriter("C:/Users/MH46/Desktop/날씨에러.xlsx") as writer:
#     etc.to_excel(writer, sheet_name='날씨에러')
#     time.to_excel(writer, sheet_name='시간통계')




# # # 비오는 날 데이터 받아오기
# # rain json 파일 받아오기
# json_path = "\\\\192.168.0.150\\완성데이터\\라벨링데이터\\차종외관인식\\"
# jpg_path = "\\\\192.168.0.150\\완성데이터\\원천데이터"
# copy_json3 = "D:/json 수정파일/car_rain/추가2/라벨링데이터/"
# # copy_json4 = "D:/json 수정파일/car_rain/8월추가/라벨링데이터/"
# copy_jpg3 = "D:/json 수정파일/car_rain/추가2/원천데이터/"
# # copy_jpg4 = "D:/json 수정파일/car_rain/8월추가/원천데이터/"
# num = 1
# weather3 = pd.DataFrame(columns=['도로명', '파일명', 'date', 'extract_time', 'weather'])
# # weather4 = pd.DataFrame(columns=['도로명', '파일명', 'date', 'extract_time', 'weather'])
#
# for (root, directory, files) in os.walk(json_path):
#     if root.endswith('번'):
#         print("검색 대상 : {}".format(root))
#         for i in os.listdir(root):
#             road = i.split('_')[2]
#             a = i.split('_')[0]
#             day = a.split('-')[1]
#
#             # 추가2
#             if (day == "220711") or (day == "220714") or (day == "220719") or (day == "220720") or (day == "220823") or (day == "220824") or (day == "220930") or (day == "221002"):
#                 with open(root + '\\' + i, 'r', encoding='UTF-8') as json_file:
#                     coco_json = json.load(json_file)
#
#                     road_directory = "[{}]{}".format(coco_json["Raw Data Info"]["location_id"],
#                                                      coco_json["Raw Data Info"]["location_name"])
#                     camera_directory = coco_json["Raw Data Info"]["cctv_number"] + '번'
#
#                     if coco_json["Raw Data Info"]["weather"] != "r":
#                         weather3.loc[num, "도로명"] = road_directory
#                         weather3.loc[num, "파일명"] = coco_json["Source Data Info"]["source_data_id"]
#                         weather3.loc[num, 'date'] = coco_json["Raw Data Info"]["date"]
#                         weather3.loc[num, "extract_time"] = coco_json["Source Data Info"]["extract_time"]
#                         weather3.loc[num, "weather"] = coco_json["Raw Data Info"]["weather"]
#
#                         if road_directory in os.listdir(copy_json3):
#                             if camera_directory in os.listdir(copy_json3 + road_directory):
#                                 shutil.copy(root + '\\' + i,
#                                             copy_json3 + road_directory + '/' + camera_directory + '/' + i)
#                                 shutil.copy(jpg_path + coco_json["Learning Data Info"]["path"] + '/' + i.split('.')[
#                                     0] + '.jpg',
#                                             copy_jpg3 + road_directory + '/' + camera_directory + '/' +
#                                             i.split('.')[0] + '.jpg')
#                                 print("완료 : {}".format(i))
#                                 num += 1
#                             if camera_directory not in os.listdir(copy_json3 + road_directory):
#                                 os.mkdir(copy_json3 + road_directory + '/' + camera_directory)
#                                 os.mkdir(copy_jpg3 + road_directory + '/' + camera_directory)
#
#                                 shutil.copy(root + '\\' + i,
#                                             copy_json3 + road_directory + '/' + camera_directory + '/' + i)
#                                 shutil.copy(jpg_path + coco_json["Learning Data Info"]["path"] + '/' + i.split('.')[
#                                     0] + '.jpg',
#                                             copy_jpg3 + road_directory + '/' + camera_directory + '/' +
#                                             i.split('.')[
#                                                 0] + '.jpg')
#                                 print("완료 : {}".format(i))
#                                 num += 1
#
#                         if road_directory not in os.listdir(copy_json3):
#                             os.mkdir(copy_json3 + road_directory)
#                             os.mkdir(copy_jpg3 + road_directory)
#                             os.mkdir(copy_json3 + road_directory + '/' + camera_directory)
#                             os.mkdir(copy_jpg3 + road_directory + '/' + camera_directory)
#
#                             shutil.copy(root + '\\' + i,
#                                         copy_json3 + road_directory + '/' + camera_directory + '/' + i)
#                             shutil.copy(
#                                 jpg_path + coco_json["Learning Data Info"]["path"] + '/' + i.split('.')[0] + '.jpg',
#                                 copy_jpg3 + road_directory + '/' + camera_directory + '/' + i.split('.')[
#                                     0] + '.jpg')
#                             print("완료 : {}".format(i))
#                             num += 1
#
# with pd.ExcelWriter("D:/json 수정파일/car_rain/car_rain_추가2.xlsx") as writer:
#     weather3.to_excel(writer, sheet_name='추가2')
#




# # # car_rain 수정
# path = "D:/json 수정파일/car_rain/car_rain_추가.xlsx"
#
# car_rain = pd.read_excel(path, sheet_name="3차수정")
# num = 1
# for index, row in car_rain.iterrows():
#     camera = row['파일명'].split('_')[3]
#     # json_path = "D:/완성데이터/라벨링데이터/차종외관인식/{}/{}/{}번/{}.json".format(row['도로'], row['도로명'], camera, row['파일명'])
#     json_path = "\\\\192.168.0.150\\완성데이터\\라벨링데이터\\차종외관인식\\{}\\{}\\{}번\\{}.json".format(row['도로'], row['도로명'], camera, row['파일명'])
#
#     with open(json_path, 'r', encoding='UTF-8') as json_file:
#         coco_json = json.load(json_file)
#
#     coco_json["Raw Data Info"]["weather"] = row['change_weather']
#
#     with open(json_path, 'w', encoding='UTF-8') as outfile:
#         json.dump(coco_json, outfile, indent=4, ensure_ascii=False)
#
#     print("수정완료 : {} {}".format(num, row['파일명']))
#     num += 1





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






# # nas 완성 폴더 개수 확인
# json_path = "\\\\192.168.0.150\\완성데이터\\라벨링데이터\\차종인식\\"
# jpg_path = "\\\\192.168.0.150\\완성데이터\\원천데이터\\차종인식\\"
# json_list = []
# jpg_list = []
#
# for (root, directory, files) in os.walk(json_path):
#     for file in files:
#         json_list.append(file)
# for (root, directory, files) in os.walk(jpg_path):
#     for file in files:
#         jpg_list.append(file)
# print("json 개수 : {}".format(len(json_list)))
# print("jpg 개수 : {}".format(len(jpg_list)))

# # 완료 meta 이동
# path = "C:/Users/MH46/Desktop/task.xlsx"
# path2 = "C:/Users/MH46/Desktop/cctv55_완료/inspection_xlsx/"
#
# aa = pd.read_excel(path)
# bb=[]
# for i in aa['task']:
#     bb.append(i)
#
# for i in os.listdir(path2):
#     if i.split('.')[0] in bb:
#         shutil.move(path2 + i, "D:/이동완료/완료_meta/" + i)
#         print(i)

