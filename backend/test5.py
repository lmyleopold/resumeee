"""
    >File Name: test5
    >Author: lmyleopold
    >Created Time: 2023/7/1 23:51
"""
import requests, pprint

# 先登陆,获取sessionid
payload = {
        'username': 'test',
        'password': '123456'
}

response = requests.post("http://localhost/applicant/signin",
                             data=payload)
retDict = response.json()
sessionid = response.cookies['sessionid']

# 再发送列出请求，注意多了 pagenum 和 pagesize
payload = {
    'action': 'list_job',
    'pagenum': 1,
    'pagesize': 2
}

response = requests.get('http://localhost/applicant/jobs/',
                          params=payload,
                          cookies={'sessionid': sessionid})

pprint.pprint(response.json())



# import requests, pprint
#
#
#
# # 再发送列出请求，注意多了 pagenum 和 pagesize
# payload = {
#     'pagenum': 1,
#     'pagesize': 2
# }
#
# response = requests.get('http://localhost/applicant/jobs/', params=payload)
#
# pprint.pprint(response.json())
