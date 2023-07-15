import json
from tqdm import tqdm
from rich import print

from resumee import Resumee
from person_info import reverse_mapping

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
    for i in tqdm(range(101, 110)):
        try:
            test = Resumee(
                    path = 'data/test/data/{0}.docx'.format(i),
                    # path = 'text_extraction/temp.pdf',
                    token = token
                )
            data[str(i)] = {
                "name": test.person_info["人物"],
                "age": test.person_info["年龄"],
                "education": reverse_mapping[test.person_info["学历"]],
                "school": test.ner["学校"],
                "work_time": test.person_info["工作年限"],
                "match_position": ""
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

        i = i + 1
    
    with open('data/test/submit.json'.format(i), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent = 4)

def test():
    test = Resumee(
                    path = 'data/dataset_CV/CV/71.docx',
                    # path = 'temp.pdf',
                    token = token
                )
    # print(test.path)
    # print(test.ext)
    # print(test.name)
    # print(test.text)
    # print(test.token)
    print('[+] NER Results: ', test.ner)
    print('[+] Information-Extraction Results: ', test.information)
    print('[+] Person-info Results: ', test.person_info)

# generate_data()
test()