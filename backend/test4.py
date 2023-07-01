"""
    >File Name: test4
    >Author: lmyleopold
    >Created Time: 2023/7/1 23:25
"""
import requests, pprint

# 先登陆,获取sessionid
payload = {
        'username': 'lmy',
        'password': '88888888'
    }

response = requests.post("http://localhost/api/mgr/signin",
                             data=payload)
retDict = response.json()
sessionid = response.cookies['sessionid']

# 再发送列出请求，注意多了 pagenum 和 pagesize
payload1 = {
    'action': 'list_applicant',
    'pagenum': 1,
    'pagesize': 2
}

payload2 = {
    'action': 'add_applicant',
    'data': {
        'name': '王燊超',
        'phonenumber': '13345679934',
        'job': '后卫'
    }
}

response = requests.get('http://localhost/api/mgr/applicants',
              params=payload1,
              cookies={'sessionid': sessionid})

response2 = requests.post('http://localhost/api/mgr/applicants',
              json=payload2,
              cookies={'sessionid': sessionid})


payload3 = {
    'action': 'list_job',
    'pagenum': 1,
    'pagesize': 2
}

response3 = requests.get('http://localhost/api/mgr/jobs',
              params=payload3,
              cookies={'sessionid': sessionid})

pprint.pprint(response3.json())
