# 55. car exterior
# path 등 변수는 상황에 맞춰 수정하여 사용하였으니 코드 실행 전 확인 할 것

# 정제 데이터 검수

import pandas as pd
import os
import shutil
import datetime


path = 'C:/Users/MH46/Desktop/cctv55/processing_check'
file_name = os.listdir(path)
file_path = []
d_today = datetime.date.today()
today = d_today.strftime('%m%d')

for i in file_name:
    file_path = path + '/' + i

    Ex55 = pd.read_excel(file_path, sheet_name=0, header=2)
    Ex55 = Ex55.dropna(how='all')
    Ex55_check = pd.read_excel("C:/Users/MH46/Desktop/cctv55/55_Meta_check.xlsx")


    class check:
        # 유효값 검사 : 해상도, 계절, 날씨, 평일/주말/휴일, 도로 유형, 교차로 유형,
        def ex55_value(self):
            a = pd.DataFrame(columns=Ex55_check.columns, index=Ex55.index)
            for i in Ex55.columns:
                if i in Ex55_check:
                    b = Ex55[~Ex55[i].isin(Ex55_check[i])][i]
                    if b.notnull().sum() >= 1:
                        a[i] = b
            aa = a.dropna(axis=1, how='all')
            value_check = aa.dropna(axis=0, how='all').fillna(" ")
            return value_check

        # 도로 유형 검사
        def ex55_road(self):
            a = pd.DataFrame(columns=['도로 유형', '교차로 유형'], index=Ex55.index)

            # aa = Ex55[(Ex55['도로 유형'] == 'CL')&(~Ex55['교차로 유형'].isin(Ex55_check['교차로 유형']))][['도로 유형', '교차로 유형']]
            bb = Ex55[(Ex55['도로 유형'] != 'cr')&(Ex55['교차로 유형'] != 0)][['도로 유형', '교차로 유형']]
            # if len(aa) >= 1:
            #     a[['도로 유형', '교차로 유형']] = aa
            if len(bb) >= 1:
                a[['도로 유형', '교차로 유형']] = bb
            road_check = a.dropna(axis=0, how='all')
            return road_check

        # 계절 일치 검사
        def ex55_season(self):
            season_check = pd.DataFrame(columns=['촬영일시', '계절'], index=Ex55.index)

            day = Ex55["촬영일시\n(yyyy-mm-dd)"]
            sp_time = Ex55[((day >= '2022-03-01') & (day <= '2022-05-31')) & (Ex55['계절'] != 'sp')]
            su_time = Ex55[((day >= '2022-06-01') & (day <= '2022-08-31')) & (Ex55['계절'] != 'su')]
            fa_time = Ex55[((day >= '2022-09-01') & (day <= '2022-11-30')) & (Ex55['계절'] != 'fa')]
            wi_time = Ex55[((day >= '2022-12-01') & (day >= '2022-12-31') | (day >= '2022-01-01') & (day < '2022-03-01'))
                           & (Ex55['계절'] != 'wi')]
            season = sp_time, su_time, fa_time, wi_time

            for i in season:
                if i['계절'].count() > 0:
                    season_check.loc[i.index]=i[['촬영일시\n(yyyy-mm-dd)', '계절']]
            season_check = season_check.dropna(axis=0, how='all')
            season_check['촬영일시'] = pd.to_datetime(season_check['촬영일시'])
            return season_check

        # 촬영장소 코드 검사
        def ex55_code(self):
            code_check = pd.DataFrame(columns=['촬영장소', '촬영장소명'], index=Ex55.index)
            for index, row in Ex55.iterrows():
                for index_check, row_check in Ex55_check.iterrows():
                    if row['촬영장소'] == row_check['촬영장소']:
                        if row['촬영장소명'] != row_check['촬영장소명']:
                            code_check.loc[index] = row[['촬영장소', '촬영장소명']]
                    if row['촬영장소명'] == row_check['촬영장소명']:
                        if row['촬영장소'] != row_check['촬영장소']:
                            code_check.loc[index] = row[['촬영장소', '촬영장소명']]
            code_check = code_check.dropna(axis=0, how='all')
            return code_check


        # # 데이터타입 검사
        # def ex55_type(self):
        #     ex55_int = 'CCTV 카메라 유형', 'CCTV 설치높이', 'CCTV 각도'
        #     Ex55["촬영일시\n(yyyy-mm-dd)"] = Ex55["촬영일시\n(yyyy-mm-dd)"].astype(str)
        #     type_err = {}
        #     for i in Ex55.columns:
        #         if Ex55[i].dtype == float:
        #             Ex55[i] = Ex55[i].astype(int)
        #             if i in ex55_int:
        #                 if Ex55[i].dtype != int:
        #                     type_err[i] = Ex55[i].dtype
        #                     Ex55[i] = Ex55[i].astype(int)
        #             elif i not in ex55_int:
        #                 if Ex55[i].dtype != str:
        #                     type_err[i] = Ex55[i].dtype
        #                     Ex55[i] = Ex55[i].astype(str)
        #     type_check = pd.DataFrame(type_err.values(), index=type_err.keys(), columns=['데이터타입'])
        #     return type_check


    # ex55_value(), ex55_type(), ex55_season()
    check = check()
    value_55 = check.ex55_value()
    road_55 = check.ex55_road()
    season_55 = check.ex55_season()
    # type_55 = check.ex55_type()
    code_55 = check.ex55_code()

    print('검수파일: {}'.format(i))

    print('_____유효 값 검사_____')
    if len(value_55) != 0:
        print(' * 오류 발견 *\n{}\n'.format(value_55))
    else:
        print('  clear\n')

    print('_____도로 유형 검사_____')
    if len(road_55) != 0:
        print(' * 오류 발견 *\n{}\n'.format(road_55))
    else:
        print('  clear\n')

    print('_____장소 코드 일치 검사_____')
    if len(code_55) != 0:
        print(' * 오류 발견 *\n{}\n'.format(code_55))
    else:
        print('  clear\n')

    print('_____계절 일치 검사_____')
    if len(season_55) != 0:
        print(' * 오류 발견 *\n{}\n'.format(season_55))
    else:
        print('  clear\n')

    # print('_____데이터 타입 검사_____')
    # if len(type_55) != 0:
    #     print(' * 오류 발견 *\n{}\n'.format(type_55))
    #     print(' * 데이터타입 재설정 완료 *\n{}\n'.format(Ex55.dtypes))
    # else:
    #     print('  clear\n')



    if len(value_55)+len(road_55)+len(code_55)+len(season_55) == 0:
        meta_name = Ex55.iloc[1]['원시 파일명'].split('_')[0] + '_' + Ex55.iloc[1]['원시 파일명'].split('_')[2] + '_' + Ex55.iloc[1]['원시 파일명'].split('_')[3]
        a = []
        for xlsx_list in os.listdir("C:/Users/MH46/Desktop/cctv55_완료/inspection_xlsx"):
            a.append(xlsx_list)
        if meta_name + '.xlsx' not in a:
            os.rename(file_path, path + '/' + meta_name + '.xlsx')
            shutil.move(path + '/' + meta_name + '.xlsx', "C:/Users/MH46/Desktop/cctv55_완료/inspection_xlsx")
            print("<< 검수결과 : clear! 파일 이동 완료 >>\n\n")
        if meta_name + '.xlsx' in a:
            os.remove(file_path)
            print("<< 검수결과 : clear! 중복 파일, 파일 삭제 >>\n\n")
    else:
        print("<< 검수 결과 : 재검토 필요 >>\n\n")




