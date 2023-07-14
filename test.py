import json
from tqdm import tqdm
from rich import print

from resumee import Resumee

token = {
            'ner': ["人物", "学校", "工作单位"], 
            'information': {
                "人物": ["性别", "出生日期", "年龄", "职务", "电话", "邮箱", "学历"],
                "学校": ["学历", "专业", "时间", "时间段"],
                "工作单位": ["职务", "时间", "时间段"]
            }
        }

def generate_data():
    for i in tqdm(range(66, 101)):
        test = Resumee(
                    path = 'data/dataset_CV/CV/{0}.docx'.format(i),
                    # path = 'text_extraction/temp.pdf',
                    token = token
                )

        # print(test.path)
        # print(test.ext)
        # print(test.name)
        # print(test.text)
        # print(test.token)
        # print('[+] NER Results: ', test.ner)
        # print('[+] Information-Extraction Results: ', test.information)

        with open('data/json/{0}.json'.format(i), 'w', encoding='utf-8') as f:
            json.dump(
                {
                    "path": test.path,
                    "text": test.text,
                    "token": test.token,
                    "result": {
                        "ner": test.ner,
                        "information": test.information}}, 
                f, ensure_ascii=False, indent = 4)

def test():
    test = Resumee(
                    path = 'data/dataset_CV/CV/71.docx',
                    # path = 'text_extraction/temp.pdf',
                    token = token
                )
    print(test.path)
    print(test.ext)
    print(test.name)
    print(test.text)
    print(test.token)
    print('[+] NER Results: ', test.ner)
    print('[+] Information-Extraction Results: ', test.information)

test()