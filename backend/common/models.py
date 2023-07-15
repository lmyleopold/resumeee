from django.db import models


# Create your models here.
class Applicant(models.Model):
    # 应聘者姓名
    ner = models.CharField(max_length=600)
    # 联系电话
    information = models.CharField(max_length=600)
    # 应聘工作
    event = models.CharField(max_length=600)
    # 人岗匹配
    match = models.CharField(max_length=100)


class Job(models.Model):
    # 工作名
    name = models.CharField(max_length=200)
    # 岗位职责
    requirements = models.TextField(max_length=400)
    # 任职要求
    responsibilities = models.TextField(max_length=400)
