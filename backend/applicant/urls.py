"""
    >File Name: urls
    >Author: lmyleopold
    >Created Time: 2023/5/14 14:54
"""

from django.urls import path
from . import sign_in_out
from . import views

urlpatterns = [
    path('', views.applicant),
    path('resume/', views.resume),
    # path('jobs/', views.listjobs),
    path('jobs/', views.jobs),
    path('upload/', views.add_applicant),
    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout),
]
