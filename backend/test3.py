"""
    >File Name: test3
    >Author: lmyleopold
    >Created Time: 2023/6/2 22:16
"""
import requests, pprint

payload = {
    'username': 'lmy',
    'password': '88888888'
}

response = requests.post('http://localhost/api/mgr/signin', data=payload)

# 检查状态码是否为200
assert response.status_code == 200

# 检查响应内容是否为JSON格式
assert response.headers.get('Content-Type') == 'application/json'

# 获取JSON响应体并进行断言
data = response.json()
assert data['ret'] == 0

pprint.pprint(data)
