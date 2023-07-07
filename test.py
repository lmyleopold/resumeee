import os
from typing import List
import torch
from transformers import AutoTokenizer

from resumee import Resumee


test = Resumee(
                path = 'data/dataset_CV/CV/16.docx',
                # path = 'text_extraction/temp.pdf',
                token = {
                    'ner': ['人物', '教育背景触发词', '工作经历触发词', '日期'], 
                    'information': {
                        '人物': ['性别', '出生年月', '年龄', '就业意向','民族', ' 电话', '政治面貌', '邮箱', '住址'],
                    }, 
                    'event': {
                        '教育背景触发词': ['学校', '阶段', '专业', '主修课程', '时间'],
                        '工作经历触发词': ['公司', '职位', '工作内容', '时间']
                    }
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