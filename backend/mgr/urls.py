"""
    >File Name: urls.py
    >Author: lmyleopold
    >Created Time: 2023/5/23 0:38
"""
from django.urls import path
from mgr import applicant

urlpatterns = [
    path('applicants', applicant.dispatcher),
]