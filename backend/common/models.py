from django.db import models

# Create your models here.
class Applicant(models.Model):
    # 应聘者姓名
    name = models.CharField(max_length=200)
    # 联系电话
    phonenumber = models.CharField(max_length=200)
    # 应聘工作
    job = models.CharField(max_length=200)
    # more to add

class Job(models.Model):
    # 工作名
    name = models.CharField(max_length=200)
    # 工作描述
    description = models.CharField(max_length=400)
