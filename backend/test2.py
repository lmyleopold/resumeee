"""
    >File Name: test2.py
    >Author: lmyleopold
    >Created Time: 2023/5/23 1:12
"""
import requests, pprint

# 构建添加 客户信息的 消息体，是json格式
payload = {
    "action": "add_applicant",
    "data": {
        "name": "奥斯卡",
        "phonenumber": "13345679934",
        "job": "中场"
    }
}

# 发送请求给web服务
response = requests.post('http://localhost/api/mgr/applicants',
              json=payload)

pprint.pprint(response.json())

# 构建查看 客户信息的消息体
response = requests.get('http://localhost/api/mgr/applicants?action=list_applicant')
# 发送请求给web服务
pprint.pprint(response.json())
