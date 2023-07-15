from docx import Document
import re
import pandas as pd

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


def jobdoc_to_csv(word_file,csv_file):
    # 打开 Word 文档
    job_data = {}
    doc = Document(word_file)
    content = ''
    for paragraph in doc.paragraphs:
        content += paragraph.text + ('\n')
        # text_content.append(paragraph.text)

    title_pattern = r"(?<=\d、)([^\n]+)(?=\n岗位职责)"
    title_matches = re.findall(title_pattern, content, re.DOTALL)
    for i in range(len(title_matches)):
        job_info = {}

        #print(i+1,"岗位名称：",title_matches[i])

        if i + 1 < len(title_matches):
            start_index = content.index(title_matches[i]) + len(title_matches[i])
            end_index = content.index(title_matches[i + 1])
            job_information = content[start_index:end_index]
            # print("-----------------------------")
            # print("岗位信息：",job_information)
            # print("-----------------------------\n")
            job_description_pattern = r"(?<=\n岗位职责[\n：:]).*(?=\n任职要求|\n职位要求)"
            job_description_match = re.findall(job_description_pattern, job_information, re.DOTALL)
            for jddescription in job_description_match:
                job_info['岗位职责'] = jddescription.strip()
                #print("岗位职责：\n",jddescription.strip())
                # print("----end-----")
            job_requirement_pattern = r"(?<=任职要求：\n|职位要求：\n|任职要求:\n|职位要求:\n).*(?=\d、)"
            job_requirement_match = re.findall(job_requirement_pattern, job_information, re.DOTALL)
            for jrdescription in job_requirement_match:
                # education_requirement_match = re.search(r".*(\b学历\b)*.", jrdescription)
                # if education_requirement_match:
                #     print("！！学历要求：",education_requirement_match.group())
                # experience_requirement_match = re.search(r"[^.!?]*学历[^.!?\n]")
                job_info['任职要求'] = jrdescription.strip()
                #print("任职要求：\n",jrdescription.strip())
                #print("----end-----\n")


        else:
            start_index = content.index(title_matches[i]) + len(title_matches[i])
            job_information = content[start_index:]
            # print("-----------------------------")
            # print("岗位信息：",job_information)
            # print("-----------------------------\n")
            job_description_pattern = r"(?<=\n岗位职责[\n：:]).*(?=任职要求：|职位要求：|任职要求:|职位要求:)"
            job_description_match = re.findall(job_description_pattern, job_information, re.DOTALL)
            for description in job_description_match:
                job_info['岗位职责'] = jddescription
                #print("岗位职责：\n", description)
            job_requirement_pattern = r"(?<=任职要求：\n|职位要求：\n|任职要求:\n|职位要求:\n).*(?=\d、)"
            job_requirement_match = re.findall(job_requirement_pattern, job_information, re.DOTALL)
            for jrdescription in job_requirement_match:
                job_info['任职要求'] = jrdescription
                #print("任职要求：\n", jrdescription)
                #print("----end-----\n")
        job_data[title_matches[i]] = job_info
    df = pd.DataFrame(columns=['岗位名称', '专业要求', '学历要求', '年龄要求', '最低工作年限', '最高工作年限'])
    for job in job_data:
        new_row = pd.DataFrame({'岗位名称': job, '专业要求': None, '学历要求': None, '年龄要求': None, '最低工作年限': None, '最高工作年限': None},
                               index=[0])
        df = pd.concat([df, new_row])
        # df = df.append({'岗位名称': job, '工作年限要求': None, '专业要求': None, '学历要求': None, '年龄要求': None}, ignore_index=True)
        # print(job)
        all_requirments = job_data[job]["任职要求"]
        # print(all_requirments)
        requirements = re.split(r'\d+[.、]', all_requirments)[1:]

        '''学历要求'''
        edubg = 0
        required_qualification_num = 0
        for requirement in requirements:
            if edubg == 0:
                requirement = requirement.strip("\n")
                education_pattern = r"(本科|硕士|博士|大专)"
                education = re.findall(education_pattern, requirement, re.IGNORECASE)
                if education and education[0] == '大专':
                    required_qualification_num = 1
                    df.loc[df['岗位名称'] == job, '学历要求'] = required_qualification_num
                    edubg = 1
                if education and education[0] == '本科':
                    required_qualification_num = 2
                    df.loc[df['岗位名称'] == job, '学历要求'] = required_qualification_num
                    edubg = 1
                if education and education[0] == '硕士':
                    required_qualification_num = 3
                    df.loc[df['岗位名称'] == job, '学历要求'] = required_qualification_num
                    edubg = 1
                if education and education[0] == '博士':
                    required_qualification_num = 4
                    df.loc[df['岗位名称'] == job, '学历要求'] = required_qualification_num
                    edubg = 1
        if edubg == 0:
            required_qualification_num = 0
            df.loc[df['岗位名称'] == job, '学历要求'] = required_qualification_num

        '''专业要求'''
        majors = []
        for requirement in requirements:
            requirement = requirement.strip("\n")
            # print(requirement)
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
            major_requirement = '无要求'
            df.loc[df['岗位名称'] == job, '专业要求'] = major_requirement

        else:
            for major in majors:
                # df.loc[df['岗位名称'] == job, '专业要求'] = ', '.join(major)
                majors_str = '、 '.join(majors)
                major_requirement = f'"{majors_str}"'
                df.loc[df['岗位名称'] == job, '专业要求'] = major_requirement

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
                            if (len(workyearnum) == 2):
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
                    age_require = int(age[0])
                    df.loc[df['岗位名称'] == job, '年龄要求'] = age_require
                    agere = 1
        if agere == 0:
            age_require = 0
            df.loc[df['岗位名称'] == job, '年龄要求'] = age_require
            # print("0,No age limitation")
        print(job,age_require,lowworkyear,highworkyear,major_requirement,required_qualification_num)

    df.to_csv(csv_file, index=False)
    print("Write done!")

    # return job_details

# Word 文件路径
word_file = "./data/岗位要求.docx"
# 保存的CSV文件路径
csv_file = "./data/job_detail.csv"
# 调用函数进行转换
jobdoc_to_csv(word_file,csv_file)

