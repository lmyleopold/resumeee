import json
import csv
from datetime import datetime

# 加载 JSON 文件
with open('./data/extraction_example/default copy.json', 'r', encoding='utf-8') as file:
    employee_info = json.load(file)

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
    print("年轻")
else:
    print("大龄")

'''单位标签'''
if len(companys) == 0:
    print("无工作经历")
if len(companys) >= 3:
    print("工作经历丰富")
with open('./data/T500companies.csv', 'r', encoding='utf-8') as file:
    # 创建 CSV 阅读器对象
    reader = csv.reader(file)
    next(reader)
    t500_companies = set(row[0] for row in reader)
for company in companys:
    if company in t500_companies:
        print("世界500强工作经验")

for company in companys:
    company_info = employee_info["result"]["information"].get(company, {})
    start_time = company_info.get("开始时间")
    end_time = company_info.get("结束时间")
    end_time_special = company_info.get("结束时间（特殊）")
    # print(company,"end time special is",end_time_special)
    # print(company,"end time is",end_time)

    if len(end_time) == 0 and end_time_special[0] == '至今':
        end_time = ['2023.04']

    year, month, = end_time[0].split(".")
    end_year = int(year)
    end_month = int(month)
    year, month, = start_time[0].split(".")
    start_year = int(year)
    start_month = int(month)
    if start_month >= end_month:
        year_diff = end_year - start_year
    else:
        year_diff = end_year - start_year + 1
    print(year_diff)

'''学校标签'''
with open('./data/985S.csv', 'r', encoding='utf-8') as file:
    # 创建 CSV 阅读器对象
    reader = csv.reader(file)
    next(reader)
    C985_school = set(row[0] for row in reader)
for school in schools:
    if any(school in c for c in C985_school):
        print("985院校")
    else:
        print("非985院校")

with open('./data/211S.csv', 'r', encoding='utf-8') as file:
    # 创建 CSV 阅读器对象
    reader = csv.reader(file)
    next(reader)
    C211_school = set(row[0] for row in reader)
for school in schools:
    if any(school in c for c in C211_school):
        print("211院校")
    else:
        print("非211院校")

for school in schools:
    school_info = employee_info["result"]["information"].get(school, {})
    start_time = school_info.get("开始时间")
    end_time = school_info.get("结束时间")
    end_time_special = school_info.get("结束时间（特殊）")
    if len(end_time) == 0 and end_time_special[0] == '至今':
        end_time = ['2023.04']
    year, month, = end_time[0].split(".")
    end_year = int(year)
    end_month = int(month)
    year, month, = start_time[0].split(".")
    start_year = int(year)
    start_month = int(month)
    if start_month >= end_month:
        year_diff = end_year - start_year
    else:
        year_diff = end_year - start_year + 1
    print(year_diff)







