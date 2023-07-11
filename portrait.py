import json
import csv
from datetime import datetime
import os
import json

# 指定存储JSON文件的文件夹路径
folder_path = './data/extraction_example'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)

        # 加载 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            employee_info = json.load(file)

        print(file_path)
        label = []
        # 访问每个人的信息并打印学校信息
        '''学校'''
        schools = employee_info["result"]["ner"].get("学校", {})
        '''工作单位'''
        companys = employee_info["result"]["ner"].get("工作单位", {})
        '''姓名'''
        name = employee_info["result"]["ner"]["人物"][0]
        '''年龄'''
        age = employee_info["result"]["information"][name]["年龄"][0]
        if age.endswith("岁"):
            age = age[:-1]
        age = int(age)
        '''项目'''


        '''年龄标签'''
        if int(age) <= 35:
            label.append("年轻")
            # print("年轻")
        else:
            label.append("大龄")
            # print("大龄")

        '''单位标签'''
        if len(companys) == 0:
            label.append("无工作经历")
            # print("无工作经历")
        if len(companys) >= 3:
            label.append("工作经历丰富")
            # print("工作经历丰富")
        with open('./data/T500companies.csv', 'r', encoding='utf-8') as file:
            # 创建 CSV 阅读器对象
            reader = csv.reader(file)
            next(reader)
            t500_companies = set(row[0] for row in reader)
        for company in companys:
            if company in t500_companies:
                label.append("世界500强工作经验")
                # print("世界500强工作经验")

        whole_work_year = 0
        year_diff_list = []
        for company in companys:
            company_info = employee_info["result"]["information"].get(company, {})
            time_gap = company_info.get("时间段")
            times = time_gap[0].split('-')
            end_time = times[1]
            start_time = times[0]
            if end_time == '至今':
                end_time = '2023.04'

            year, month = end_time.split(".")
            end_year = int(year)
            end_month = int(month)

            year, month = start_time.split(".")
            start_year = int(year)
            start_month = int(month)

            if start_month >= end_month:
                year_diff = end_year - start_year
            else:
                year_diff = end_year - start_year + 1
            # print(year_diff)
            year_diff_list.append(year_diff)
            whole_work_year += year_diff
        # print(whole_work_year)
        if whole_work_year >= 5:
            label.append("工作年数长")
        if len(year_diff_list):
            average_work_year = whole_work_year/len(year_diff_list)
            if average_work_year > 3:
                label.append("工作稳定")
            else:
                label.append("工作不稳定")


        '''学校标签'''
        with open('./data/985S.csv', 'r', encoding='utf-8') as file:
            # 创建 CSV 阅读器对象
            reader = csv.reader(file)
            next(reader)
            C985_school = set(row[0] for row in reader)
        for school in schools:
            if any(school in c for c in C985_school):
                # print("985院校")
                label.append("985院校")
            else:
                # print("非985院校")
                label.append("非985院校")

        with open('./data/211S.csv', 'r', encoding='utf-8') as file:
            # 创建 CSV 阅读器对象
            reader = csv.reader(file)
            next(reader)
            C211_school = set(row[0] for row in reader)
        for school in schools:
            if any(school in c for c in C211_school):
                # print("211院校")
                label.append("211院校")
            else:
                # print("非211院校")
                label.append("非211院校")

        # for school in schools:
        #     school_info = employee_info["result"]["information"].get(school, {})
        #     start_time = school_info.get("开始时间")
        #     end_time = school_info.get("结束时间")
        #     end_time_special = school_info.get("结束时间（特殊）")
        #     if len(end_time) == 0 and end_time_special[0] == '至今':
        #         end_time = ['2023.04']
        #     year, month, = end_time[0].split(".")
        #     end_year = int(year)
        #     end_month = int(month)
        #     year, month, = start_time[0].split(".")
        #     start_year = int(year)
        #     start_month = int(month)
        #     if start_month >= end_month:
        #         year_diff = end_year - start_year
        #     else:
        #         year_diff = end_year - start_year + 1
        #     print(year_diff)

        print(label)
        print("---------")




