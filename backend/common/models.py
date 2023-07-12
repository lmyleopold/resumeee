from django.db import models


# Create your models here.
class Applicant(models.Model):
    # 应聘者姓名/学校/岗位
    ner = models.CharField(max_length=200)
    # 信息
    information = models.CharField(max_length=600)
    # 事迹
    event = models.CharField(max_length=400)
    # more to add


class Job(models.Model):
    # 工作名
    name = models.CharField(max_length=200)
    # 工作描述
    # description = models.CharField(max_length=400)
    # 岗位职责
    requirements = models.TextField(max_length=400)
    # 任职要求
    responsibilities = models.TextField(max_length=400)
