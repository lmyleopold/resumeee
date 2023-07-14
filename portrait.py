import json
import csv
from datetime import datetime
import os
import json
import csv

# 指定要保存的 CSV 文件路径
csv_file = './data/labels.csv'

# 打开 CSV 文件进行写入
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # 写入表头
    writer.writerow(['人物', '标签'])

    # 指定存储JSON文件的文件夹路径
    folder_path = './data/json'

    count = 0
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
            name = employee_info["result"]["ner"]["人物"]
            if len(name) == 0:
                name = "***"
            else:
                name = name[0]


            '''年龄'''
            try:
                age = employee_info["result"]["information"][name]["年龄"]
                if len(age) == 1:
                    age = age[0]
                    try:
                        if age.endswith("岁"):
                            age = age[:-1]
                        age = int(age)
                    except ValueError:
                        age = None
                else:
                    age = None
            except KeyError:
                age = None
            # print(age)
            '''项目'''


            '''年龄标签'''
            if age is not None:
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

                if(len(time_gap) == 1): # 判断时间段是否为一个
                    times = time_gap[0].split('-')
                    # print(times)
                    if len(times) != 2:# 如果时间段不能通过-分离
                        times = time_gap[0].split('–')
                        if len(times) != 2:
                            companys.remove(company) # 移除该时间段
                            break
                    end_time = times[1]
                    start_time = times[0]
                    # print("成功读取时间段，成功通过-分离时间段",start_time,"-",end_time)
                    if end_time == '至今' or end_time == '至今)':
                        end_time = '2023.04'
                else: # 时间段有2个或0个
                    times = company_info.get("时间")
                    if(len(times) != 2):
                        companys.remove(company)
                        break
                    end_time = times[1]
                    start_time = times[0]
                    # print("成功读取时间，成功下标得到时间", start_time, "-", end_time)
                    # print(start_time,"-",end_time)
                    # print("end_time is",end_time)


                try:
                    if len(end_time.split(".")) == 2:
                        year, month = end_time.split(".")
                        end_year = int(year)
                        # print("结束年份为",end_year)
                        end_month = int(month)
                        # print("结束月份为",end_month)
                    else:
                        end_year = end_time.split(".")[0]
                        end_year = int(end_year)
                        end_month = 13
                except ValueError:
                    year = end_time.split("年")[0]
                    end_year = int(year)
                    # print("结束年份为", end_year)
                    month = end_time.split("年")[1].split("月")[0]
                    end_month = int(month)
                    # print("结束月份为", end_month)

                try:
                    if len(start_time.split(".")) == 2:
                        year, month = start_time.split(".")
                        start_year = int(year)
                        # print("结束年份为",start_year)
                        start_month = int(month)
                        # print("结束月份为",start_month)
                    else:
                        start_year = start_time.split(".")[0]
                        start_year = int(start_year)
                        start_month = 13
                except ValueError:
                    year = start_time.split("年")[0]
                    start_year = int(year)
                    # print("开始年份为", start_year)
                    month = start_time.split("年")[1].split("月")[0]
                    start_month = int(month)
                    # print("开始月份为", start_month)

                # year, month = start_time.split(".")
                # start_year = int(year)
                # start_month = int(month)

                if start_month >= end_month:
                    year_diff = end_year - start_year
                else:
                    year_diff = end_year - start_year + 1
                # print("年差",year_diff)
                year_diff_list.append(year_diff)
                whole_work_year += year_diff
            # print(whole_work_year)
            if whole_work_year >= 5:
                label.append("工作年份长")
            if whole_work_year <= 2:
                label.append("工作年份短")
            if len(year_diff_list):

                average_work_year = whole_work_year/len(year_diff_list)
                # print("平均工作年长", average_work_year)
                if average_work_year >= 3:
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
                try:
                    qualifications = employee_info["result"]["information"][school]['学历']
                    if len(qualifications) == 0:
                        qualifications = None
                        break
                    # print(qualifications)
                    if any(school in c for c in C985_school):
                        # print("985院校")
                        for qualification in qualifications:

                            if "985院校"+qualification not in label:
                                label.append("985院校"+qualification)
                    else:
                        # print("非985院校")
                        for qualification in qualifications:
                            if "非985院校"+qualification not in label:
                                label.append("非985院校"+qualification)
                except KeyError:
                    break


            with open('./data/211S.csv', 'r', encoding='utf-8') as file:
                # 创建 CSV 阅读器对象
                reader = csv.reader(file)
                next(reader)
                C211_school = set(row[0] for row in reader)
            for school in schools:
                try:
                    qualifications = employee_info["result"]["information"][school]['学历']
                    if len(qualifications) == 0:
                        qualifications = None
                        break

                    if any(school in c for c in C211_school):
                        # print("211院校")
                        for qualification in qualifications:
                            if "211院校"+qualification not in label:
                                label.append("211院校"+qualification)
                    else:
                        # print("非211院校")
                        for qualification in qualifications:
                            if "非211院校"+qualification not in label:
                                label.append("非211院校"+qualification)

                except KeyError:
                    break

            # for school in schools:
            #     qualification = employee_info["result"]["information"][school]['学历']
            #     print(qualification)
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

            writer.writerow([name, label])
            print(label)
            print("---------")

