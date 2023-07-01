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
pprint.pprint(response.json())
