"""
    >File Name: test1.py
    >Author: lmyleopold
    >Created Time: 2023/5/23 0:58
"""
import pprint
import requests

response = requests.get('http://localhost/api/mgr/applicants?action=list_applicant')
pprint.pprint(response.json())
