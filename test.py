import os
from typing import List
import torch
from transformers import AutoTokenizer

from resumee import Resumee


test = Resumee(
                path = 'data/dataset_CV/CV/71.docx',
                # path = 'text_extraction/temp.pdf',
                token = {
                    'ner': ["人物", "学校", "工作单位"], 
                    'information': {
                        "人物": ["性别", "出生日期", "年龄", "职务", "电话", "邮箱", "学历"],
                        "学校": ["学历", "专业", "时间", "时间段"],
                        "工作单位": ["职务", "时间", "时间段"]
                    }, 
                    'event': {} # Temporarily not used
                }
            )

print(test.path)
print(test.ext)
print(test.name)
print(test.text)
print(test.token)
print('[+] NER Results: ', test.ner)
print('[+] Information-Extraction Results: ', test.information)
print('[+] Event-Extraction Results: ', test.event)