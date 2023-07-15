qualification_mapping = {
    "中专": "1",
    "高中": "2",
    "大专": "3",
    "本科": "4",
    "硕士": "5",
    "博士": "6",
}

reverse_mapping = {
    "0": "无学历",
    "1": "中专",
    "2": "高中",
    "3": "大专",
    "4": "本科",
    "5": "硕士",
    "6": "博士",

}

def get_person_info(ner, information):
    '''学历'''
    schools = ner.get("学校", {})
    for school in schools:
        # print(school)
        try:
            qualifications = information[school]['学历']
            quanlification_list = []
            for qualification in qualifications:
                if qualification in qualification_mapping:
                    qualification = qualification_mapping[qualification]
                    quanlification_list.append(qualification)
        except KeyError:
            qualifications = None
            highest_edu_num = "0"

    try:
        highest_edu_num = max(quanlification_list)
        # print(max(quanlification_list))
    except ValueError:
        highest_edu_num = "0"

    '''最高学历学校'''
    highest_edu = reverse_mapping[highest_edu_num]
    highest_school = '某学校'
    for school in schools:
        if school in information:
            education = information[school]['学历']
            try:
                if highest_edu in education:
                    highest_school = school
                else:
                    highest_school = school
            except TypeError:
                highest_school = '某学校'


    '''专业'''
    major_list = []
    for school in schools:
        try:
            majors = information[school]['专业']
            for major in majors:
                major_list.append(major)
        except KeyError:
            break

    '''工作年数'''
    whole_work_year = 0
    year_diff_list = []
    companys = ner.get("工作单位", {})
    for company in companys:
        company_info = information.get(company, {})
        time_gap = company_info.get("时间段")

        if (len(time_gap) == 1):  # 判断时间段是否为一个
            times = time_gap[0].split('-')
            # print(times)
            if len(times) != 2:  # 如果时间段不能通过-分离
                times = time_gap[0].split('–')
                if len(times) != 2:
                    companys.remove(company)  # 移除该时间段
                    break
            end_time = times[1]
            start_time = times[0]
            # print("成功读取时间段，成功通过-分离时间段",start_time,"-",end_time)
            if end_time == '至今' or end_time == '至今)':
                end_time = '2023.04'
        else:  # 时间段有2个或0个
            times = company_info.get("时间")
            if (len(times) != 2):
                end_time = '2000.01'
                start_time = '2000.02'
            else:
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
            try:
                year = end_time.split("年")[0]
                end_year = int(year)
                # print("结束年份为", end_year)
                month = end_time.split("年")[1].split("月")[0]
                end_month = int(month)
                # print("结束月份为", end_month)
            except ValueError:
                if len(end_time.split("/")) == 2:
                    year, month = end_time.split("/")
                    end_year = int(year)
                    # print("结束年份为",end_year)
                    end_month = int(month)
                    # print("结束月份为",end_month)
                else:
                    end_year = end_time.split("/")[0]
                    end_year = int(end_year)
                    end_month = 13

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
            try:
                year = start_time.split("年")[0]
                start_year = int(year)
                # print("开始年份为", start_year)
                month = start_time.split("年")[1].split("月")[0]
                start_month = int(month)
                # print("开始月份为", start_month)
            except ValueError:
                if len(start_time.split("/")) == 2:
                    year, month = start_time.split("/")
                    start_year = int(year)
                    # print("结束年份为",end_year)
                    start_month = int(month)
                    # print("结束月份为",end_month)
                else:
                    start_year = start_time.split("/")[0]
                    start_year = int(start_year)
                    start_month = 13

        if start_month >= end_month:
            year_diff = end_year - start_year
        else:
            year_diff = end_year - start_year + 1
        # print("年差",year_diff)
        year_diff_list.append(year_diff)
        whole_work_year += year_diff

    '''年龄'''
    name = ner["人物"]
    target_job_list = []
    if len(name) == 0:
        name = "***"
    else:
        name = name[0]
    try:
        age_list = information[name]["年龄"]
        for age in age_list:
            try:
                if age.endswith("岁"):
                    age = age[:-1]
                age = int(age)
                if age < 18 or age > 60:
                    age = 0
                break
            except ValueError:
                bday_list = information[name]["出生日期"]
                bday_cal_list = []
                for bday in bday_list:
                    month = 0
                    year = 0
                    day = 0
                    if '.' in bday:
                        try:
                            year, month, day = bday.split(".")
                            year = int(year)
                            month = int(month)
                            day = int(day)
                        except ValueError:
                            year, month = bday.split(".")
                            year = int(year)
                            month = int(month)
                            day = 0
                    if '/' in bday:
                        year, month, day = bday.split("/")
                        year = int(year)
                        month = int(month)
                        day = int(day)
                    if '年' in bday:
                        year = bday.split("年")[0]
                        month = bday.split("年")[1].split("月")[0]
                        year = int(year)
                        try:
                            month = int(month)
                            day = int(day)
                        except ValueError:  # 处理2000年
                            month = 0
                            day = 0

                    '''caculation(以2023.4.1计算)'''
                    if month >= 4:
                        age = 2023 - year
                    else:
                        age = 2023 - year + 1
                    if age < 18 or age > 60:
                        age = 0
                    bday_cal_list.append(age)
                if len(bday_cal_list):
                    age = max(bday_cal_list)
                else:
                    age = 0

        '''任职意向'''
        for taget_jobs in information[name]["职务"]:
            target_job_list.append(taget_jobs)
    except KeyError:
        age = 0
        target_job = None
    # print(age)
    # print(target_job)

    person_info = {
        '人物': name, 
        '年龄': age, 
        '工作年限': whole_work_year,
        '专业': ", ".join(major_list), 
        '学历': highest_edu_num, 
        '任职意向': ", ".join(target_job_list),
        '最高学历学校': highest_school

    }
    return person_info

# folder_path = './data/json'
# csv_file = "./data/json/recruit_output.csv"
# create_person_table(folder_path,csv_file)
# print('Done')