import json
from tqdm import tqdm
from rich import print

from extraction.jobs import Jobs
from extraction.resumee import Resumee
from extraction.person_info import reverse_mapping

token = {
            'ner': ["人物", "学校", "工作单位"], 
            'information': {
                "人物": ["性别", "出生日期", "年龄", "职务", "电话", "邮箱", "学历"],
                "学校": ["学历", "专业", "时间", "时间段"],
                "工作单位": ["职务", "时间", "时间段"]
            }
        }

def generate_data():
    data = {}
    jobs = Jobs('data/岗位要求.docx')
    for i in tqdm(range(101, 301)):
        try:
            test = Resumee(
                    path = 'data/test/data/{0}.docx'.format(i),
                    # path = 'text_extraction/temp.pdf',
                    token = token
                )
            fit = test.fit(jobs.job_info)
            data[str(i)] = {
                "name": test.person_info["人物"],
                "age": test.person_info["年龄"],
                "education": reverse_mapping[test.person_info["学历"]],
                "school": test.person_info["最高学历学校"],
                "work_time": test.person_info["工作年限"],
                "match_position": "" if len(fit) == 0 else fit[0]
            }
        except:
            data[str(i)] = {
                "name": "",
                "age": "",
                "education": "",
                "school": "",
                "work_time": "",
                "match_position": ""
            }

        if i % 50 == 0:
            with open('data/test/submit_{0}.json'.format(i), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent = 4)

def test():
    test = Resumee(
                    # path = 'data/test_ocr.pdf',
                    path = 'data/test/data/276.docx',
                    # path = 'temp.pdf',
                    token = token
                )

    print(test.path)
    print(test.ext)
    print(test.name)
    print(test.text)
    print(test.token)
    print('[+] NER Results: ', test.ner)
    print('[+] Information-Extraction Results: ', test.information)
    print('[+] Person-info Results: ', test.person_info)
    print('[+] Portrait Results: ', test.label)

    test_job = Jobs('data/岗位要求.docx')
    # print(test_job.description['产品运营'])
    # print(test_job.job_info['产品运营'])

    print('[+] Job_fit Results: ', test.fit(test_job.job_info))

# generate_data()
test()