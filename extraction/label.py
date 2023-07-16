import csv

def portrait(ner, information, person_info):
    label = []

    '''姓名'''
    name = ner["人物"]
    if len(name) == 0:
        name = "***"
    else:
        name = name[0]
    '''学校'''
    schools = ner.get("学校", {})
    '''工作单位'''
    companys = ner.get("工作单位", {})

    '''年龄'''
    try:
        age = person_info["年龄"]
    except KeyError:
        age = None

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

    # 工作年份
    whole_work_year = person_info["工作年限"]
    if whole_work_year >= 5:
        label.append("工作年份长")
    if whole_work_year <= 2:
        label.append("工作年份短")


    '''学校标签'''
    with open('./data/985S.csv', 'r', encoding='utf-8') as file:
        # 创建 CSV 阅读器对象
        reader = csv.reader(file)
        next(reader)
        C985_school = set(row[0] for row in reader)
    for school in schools:
        try:
            qualifications = information[school]['学历']
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
            qualifications = information[school]['学历']
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
    
    return label

