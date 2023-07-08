"""
    >File Name: job_data
    >Author: lmyleopold
    >Created Time: 2023/7/8 23:00
"""

import json

import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc
execute_from_command_line(sys.argv)

from common.models import Job

tf = open("job_data.json", "r", encoding="utf-8")  # use job_data.json in ../data/
jobs_data = json.load(tf)
print(jobs_data)

for job_name, job_data in jobs_data.items():
    job = Job(name=job_name, responsibilities=job_data['岗位职责'], requirements=job_data['任职要求'])
    job.save()
