"""
    >File Name: urls
    >Author: lmyleopold
    >Created Time: 2023/5/14 14:54
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.applicant),
    path('resume/', views.resume),
    path('jobs/', views.listjobs),
]
