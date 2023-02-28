# 55. car exterior
# path 등 변수는 상황에 맞춰 수정하여 사용하였으니 코드 실행 전 확인 할 것

# coco json 크롤링
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import zipfile
import os
from selenium.webdriver.common.keys import Keys
import pandas as pd



file_path = 'C:/Users/MH46/Desktop/coco_list.xlsx'
coco_list = pd.read_excel(file_path, sheet_name= 0)


driver = webdriver.Chrome("C:/Users/MH46/chromedriver.exe")
# url = "http://210.121.177.103:20256/tasks?page=1" #"http://124.194.100.230:20255/tasks?page=1"
url = "http://210.121.223.158:20257/tasks?page=1"
login_data = {"username" : "hyein", "password" : "dbsdbsdbs"} #{"username" : "테스트3", "password" : "xptmxm0514"}

driver.get(url)
time.sleep(1.5)

# 로그인
driver.find_element(By.ID,'username').send_keys(login_data.get('username'))
driver.find_element(By.ID,'password').send_keys(login_data.get('password'))
time.sleep(1.0)
driver.find_element(By.CLASS_NAME, 'ant-btn').click()
time.sleep(3.0)

# 검색
for index, row in coco_list.iterrows():
    # if row['서버'] == '신':
    if row['서버'] == '통합':

        # task 검색
        driver.find_element(By.CLASS_NAME, 'ant-input').send_keys(row['task'])
        time.sleep(1.0)
        driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div[1]/div/div[1]/span/span/span/button/span').click()
        time.sleep(2.5)

        # Actions - Export
        driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div[2]/div/div/div[4]/div[2]/div').click()
        time.sleep(1.5)
        driver.find_element(By.XPATH, '/html/body/div[4]/div/div/ul/li[2]').click()
        time.sleep(1.0)

        # coco
        driver.find_element(By.XPATH, '//*[@id="Export dataset"]/div[1]/div[2]/div/div/div/div').click()
        time.sleep(1.0)
        driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[2]/div[1]/div/div/div[3]/div').click()
        time.sleep(1.0)
        driver.find_element(By.XPATH, '//*[@id="Export dataset_customName"]').send_keys(row['task'])
        time.sleep(1.0)
        driver.find_element(By.XPATH, '//*[@id="Export dataset_saveImages"]').click()
        time.sleep(1.0)
        driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/div/div[2]/div[3]/button[2]').click()
        time.sleep(20.0)
        driver.refresh()
        time.sleep(1.0)
        driver.find_element(By.CLASS_NAME, 'ant-input').send_keys(Keys.CONTROL + 'a')
        time.sleep(1.0)
        driver.find_element(By.CLASS_NAME, 'ant-input').send_keys(Keys.DELETE)
        time.sleep(1.0)

driver.quit()

# 압축해제 및 json작업 대상 폴더 이동/파일명 변경
for index, row in coco_list.iterrows():
    print(row['task'])
    if row['서버'] == '신':
        zipfile.ZipFile('C:/Users/MH46/Downloads/' + row['task'].lower() + '.zip').extract('annotations/instances_default.json', 'C:/Users/MH46/Desktop/cctv55/inspection_json')
        os.rename('C:/Users/MH46/Desktop/cctv55/inspection_json/annotations/instances_default.json', 'C:/Users/MH46/Desktop/cctv55/inspection_json/' + row['task'] + '.json')
        os.rmdir('C:/Users/MH46/Desktop/cctv55/inspection_json/annotations')
        zipfile.ZipFile('C:/Users/MH46/Downloads/' + row['task'].lower() + '.zip').extractall('C:/Users/MH46/Desktop/cctv55/jpg')

        for i in os.listdir('C:/Users/MH46/Desktop/cctv55/jpg/images/'):
            shutil.move('C:/Users/MH46/Desktop/cctv55/jpg/images/'+ i, 'C:/Users/MH46/Desktop/cctv55/jpg/' + i)
        os.rmdir('C:/Users/MH46/Desktop/cctv55/jpg/images/')
        shutil.rmtree('C:/Users/MH46/Desktop/cctv55/jpg/annotations')

    if row['서버'] == '통합':
        zipfile.ZipFile('C:/Users/MH46/Downloads/' + row['task'].lower() + '.zip').extract('annotations/instances_default.json', 'C:/Users/MH46/Desktop/cctv55/inspection_json')
        os.rename('C:/Users/MH46/Desktop/cctv55/inspection_json/annotations/instances_default.json', 'C:/Users/MH46/Desktop/cctv55/inspection_json/' + row['task'] + '.json')
        os.rmdir('C:/Users/MH46/Desktop/cctv55/inspection_json/annotations')
        zipfile.ZipFile('C:/Users/MH46/Downloads/' + row['task'].lower() + '.zip').extractall('C:/Users/MH46/Desktop/cctv55/jpg')

        for i in os.listdir('C:/Users/MH46/Desktop/cctv55/jpg/images/'):
            shutil.move('C:/Users/MH46/Desktop/cctv55/jpg/images/'+ i, 'C:/Users/MH46/Desktop/cctv55/jpg/' + i)
        os.rmdir('C:/Users/MH46/Desktop/cctv55/jpg/images/')
        shutil.rmtree('C:/Users/MH46/Desktop/cctv55/jpg/annotations')

    if row['서버'] == '구':
        zipfile.ZipFile('C:/Users/MH46/Downloads/' + row['task'].lower() + '.zip').extract(
            'annotations/instances_default.json', 'C:/Users/MH46/Desktop/cctv55/inspection_json')
        os.rename('C:/Users/MH46/Desktop/cctv55/inspection_json/annotations/instances_default.json',
                  'C:/Users/MH46/Desktop/cctv55/inspection_json/' + row['task'] + '.json')
        os.rmdir('C:/Users/MH46/Desktop/cctv55/inspection_json/annotations')





