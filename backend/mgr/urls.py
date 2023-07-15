"""
    >File Name: urls.py
    >Author: lmyleopold
    >Created Time: 2023/5/23 0:38
"""
from django.urls import path
from mgr import applicant
from mgr import job
from mgr import sign_in_out

urlpatterns = [
    path('applicants', applicant.dispatcher),
    path('jobs/upload', job.addjob),
    path('jobs', job.dispatcher),
    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout),
]
