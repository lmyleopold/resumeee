"""
    >File Name: test_uploadApp
    >Author: lmyleopold
    >Created Time: 2023/7/15 10:50
"""

import requests

# 定义上传文件的路径
file_path = '../data/dataset_CV/CV/97.docx'
# 构建请求数据
files = {'file': open(file_path, 'rb')}
# 发送上传文件的请求
response = requests.post('http://localhost/applicant/upload/', files=files)

# 处理响应结果
print(response.status_code)
print(response.json())
