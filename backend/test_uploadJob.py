"""
    >File Name: test_uploadJob
    >Author: lmyleopold
    >Created Time: 2023/7/16 3:08
"""

import requests

# payload = {
#         'username': 'lmy',
#         'password': '88888888'
#     }
# response = requests.post("http://localhost/api/mgr/signin",
#                              data=payload)
# sessionid = response.cookies['sessionid']

# 定义上传文件的路径
file_path = '../data/岗位要求.docx'
# 构建请求数据
files = {'file': open(file_path, 'rb')}
# 发送上传文件的请求
response = requests.post('http://localhost/api/mgr/jobs/upload', files=files)

# response = requests.post('http://localhost/api/mgr/jobs?action=add_job',
#               files=files,
#               cookies={'sessionid': sessionid})

# 处理响应结果
print(response.status_code)
print(response.json())
