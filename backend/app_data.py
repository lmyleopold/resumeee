"""
    >File Name: app_data
    >Author: lmyleopold
    >Created Time: 2023/7/12 17:03
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

from common.models import Applicant

tf = open("../data/extraction_example/98.json", "r", encoding="utf-8")  # use *.json in ../data/
apps_data = json.load(tf)['result']
# print(apps_data)
ner = ''
info = ''
event = ''
for _, data in apps_data.items():
    if _ == 'ner':
        ner = data
    elif _ == 'information':
        info = data
    elif _ == 'event':
        event = data
app = Applicant(ner=ner, information=info, event=event)
app.save()
