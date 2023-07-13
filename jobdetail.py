import json
import re
import pandas as pd
import numpy as np

# 数字映射字典
number_mapping = {
    "一": "1",
    "两": "2",
    "三": "3",
    "四": "4",
    "五": "5",
    "六": "6",
    "七": "7",
    "八": "8",
    "九": "9"
}

df = pd.DataFrame(columns=['岗位名称',  '专业要求', '学历要求', '年龄要求','最低工作年限','最高工作年限'])

# 打开JSON文件
with open('./data/job_data.json', 'r') as f:
    data = json.load(f)

for job in data:
    new_row = pd.DataFrame({'岗位名称': job, '专业要求': None, '学历要求': None, '年龄要求': None, '最低工作年限': None, '最高工作年限':None }, index=[0])
    df = pd.concat([df, new_row])
    # df = df.append({'岗位名称': job, '工作年限要求': None, '专业要求': None, '学历要求': None, '年龄要求': None}, ignore_index=True)
    print(job)
    all_requirments = data[job]["任职要求"]
    #print(all_requirments)
    requirements = re.split(r'\d+[.、]', all_requirments)[1:]

    '''学历要求'''
    edubg = 0
    for requirement in requirements:
        if edubg == 0:
            requirement = requirement.strip("\n")
            education_pattern = r"(本科|硕士|博士|大专)"
            education = re.findall(education_pattern, requirement, re.IGNORECASE)
            if education and education[0] == '大专':
                df.loc[df['岗位名称'] == job, '学历要求'] = 1
                edubg = 1
            if education and education[0] == '本科':
                df.loc[df['岗位名称'] == job, '学历要求'] = 2
                edubg = 1
            if education and education[0] == '硕士':
                df.loc[df['岗位名称'] == job, '学历要求'] = 3
                edubg = 1
            if education and education[0] == '博士':
                df.loc[df['岗位名称'] == job, '学历要求'] = 4
                edubg = 1
    if edubg == 0:
        df.loc[df['岗位名称'] == job, '学历要求'] = 0

    '''专业要求'''
    majors = []
    for requirement in requirements:
        requirement = requirement.strip("\n")
        #print(requirement)
        major_sentence_pattern = r"(?:(?<=，|；|:|;|\n)|^).*?专业.*(?=，|；|.|;|\n)"
        major_sentence = re.findall(major_sentence_pattern, requirement, re.IGNORECASE)
        if major_sentence:
            front_major_pattern = r"((?<=专业要求:).*(?=，|；|.|:|;|$))"
            front_major = re.findall(front_major_pattern, requirement, re.IGNORECASE)
            if front_major:
                majors = front_major[0].split('、')
                for i in range(len(majors)):
                    if re.search(r'[^\w\s]', majors[i]):
                        majors[i] = majors[1].replace('.', '')
            rear_major_pattern = r"(?<=\b)\w+(?=专业)"
            rear_major = re.findall(rear_major_pattern, requirement, re.IGNORECASE)
            if rear_major:
                majors.append(rear_major[0])
    if len(majors) == 0:
        df.loc[df['岗位名称'] == job, '专业要求'] = '无要求'
    else:
        for major in majors:
            print(major)
            # df.loc[df['岗位名称'] == job, '专业要求'] = ', '.join(major)
            majors_str = '、 '.join(majors)
            df.loc[df['岗位名称'] == job, '专业要求'] = f'"{majors_str}"'

    '''工作年限要求'''
    wyre = 0
    for requirement in requirements:
        if wyre == 0:
            requirement = requirement.strip("\n")
            # print(requirement)
            workyear_sentence_pattern = r"(?:(?<=，|；|:|;|\n)|^).*?年.*?(?=，|；|:|;|\n|$)"
            # workyear_sentence_pattern = r"(?:(?<=，|；|:|;|\n)|^).*?(?:\d+年|一年|两年|三年|四年|五年|六年|七年|八年|九年|十年|\d-\d年).*?(?=，|；|:|;|\n|$)"
            workyear_sentence = re.findall(workyear_sentence_pattern, requirement, re.IGNORECASE)
            if workyear_sentence:
                workyear_pattern = r"\d +年|\d+年|一年|两年|三年|四年|五年|六年|七年|八年|九年|十年|\d-\d年"
                workyear = re.findall(workyear_pattern, workyear_sentence[0], re.IGNORECASE)
                if workyear:
                    numplusyear_pattern = r"\d+|一+|两+|三+|四+|五+|六+|七+|八+|九+|十+"
                    workyearnum = re.findall(numplusyear_pattern, workyear[0], re.IGNORECASE)
                    if workyearnum:
                        if(len(workyearnum) == 2):
                            lowworkyear = workyearnum[0]
                            highworkyear = workyearnum[1]
                            df.loc[df['岗位名称'] == job, '最低工作年限'] = lowworkyear
                            df.loc[df['岗位名称'] == job, '最高工作年限'] = highworkyear
                            # print(lowworkyear,"-",highworkyear)
                            wyre = 1
                        else:
                            if workyearnum[0] in number_mapping:
                                workyearnum[0] = number_mapping[workyearnum[0]]
                            lowworkyear = int(workyearnum[0])
                            highworkyear = 99
                            df.loc[df['岗位名称'] == job, '最低工作年限'] = lowworkyear
                            df.loc[df['岗位名称'] == job, '最高工作年限'] = highworkyear
                            # print(lowworkyear,"-",highworkyear)
                            wyre = 1
    if wyre == 0:
        lowworkyear = 0
        highworkyear = 99
        df.loc[df['岗位名称'] == job, '最低工作年限'] = lowworkyear
        df.loc[df['岗位名称'] == job, '最高工作年限'] = highworkyear
        # print(lowworkyear, "-", highworkyear,"No work year requirement")

    '''年龄要求'''
    agere = 0
    for requirement in requirements:
        if agere == 0:
            requirement = requirement.strip("\n")
            age_phase_pattern = r"\d+岁"
            age_phase = re.findall(age_phase_pattern, requirement, re.IGNORECASE)
            if age_phase:
                age_pattern = r"\d+"
                age = re.findall(age_pattern, requirement, re.IGNORECASE)
                age_require = age[0]
                df.loc[df['岗位名称'] == job, '年龄要求'] = age_require
                # print(age_require)
                agere = 1
    if agere == 0:
        df.loc[df['岗位名称'] == job, '年龄要求'] = 0
        # print("0,No age limitation")

# 将数据写入新的CSV文件
df.to_csv('./data/job_detail.csv', index=False)
print("Write done!")
