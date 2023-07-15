# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from common.models import Job
from common.models import Applicant
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from django.conf import settings
import json
from tqdm import tqdm
from rich import print
import os
from extraction.resumee import Resumee
from extraction.jobs import Jobs
from extraction.person_info import reverse_mapping


token = {
            'ner': ["人物", "学校", "工作单位"],
            'information': {
                "人物": ["性别", "出生日期", "年龄", "职务", "电话", "邮箱", "学历"],
                "学校": ["学历", "专业", "时间", "时间段"],
                "工作单位": ["职务", "时间", "时间段"]
            }
        }


def applicant(request):
    return HttpResponse("这里是申请者所看到的界面")


def resume(request):
    return HttpResponse("这里提交和查看已提交简历")


def jobs(request):
    # 根据session判断用户是否是登录的申请者用户
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': '/applicant/sign.html'},
            status=302)

    if request.session['usertype'] != 'usr':
        return JsonResponse({
            'ret': 302,
            'msg': '用户非usr类型',
            'redirect': '/applicant/sign.html'},
            status=302)
    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET
    try:
        # 要获取的第几页
        print('=========='+str(request)+'==============')
        pagenum = request.params['pagenum']
        # 每页要显示多少条记录
        pagesize = request.params['pagesize']
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        qs = Job.objects.values()
        # 使用分页对象，设定每页多少条记录
        pgnt = Paginator(qs, pagesize)
        # 从数据库中读取数据，指定读取其中第几页
        page = pgnt.page(pagenum)
        # 将 QuerySet 对象 转化为 list 类型
        retlist = list(page)

        # total指定了 一共有多少数据
        return JsonResponse({'ret': 0, 'retlist': retlist, 'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n'})


def add_applicant1(request):

    uploaded_file = request.FILES['file']
    file_path = os.path.join(settings.TEMP_UPLOAD_DIR, uploaded_file.name)

    with open(file_path, 'wb') as file:
        for chunk in uploaded_file.chunks():
            file.write(chunk)

    test = Resumee(
        # path='../temp_uploads/'+uploaded_file.name,
        path='../../data/dataset_CV/CV/71.docx',
        token=token
    )
    print('[+] NER Results: ', test.ner)
    print('[+] Information-Extraction Results: ', test.information)
    print('[+] Person-info Results: ', test.person_info)

    return JsonResponse({'ret': 0, 'id': 666})

    # record = Applicant.objects.create(ner=info['ner'],
    #                                   information=info['information'],
    #                                   event=info['event'])
    # return JsonResponse({'ret': 0, 'id': record.id})


import threading


def add_applicant(request):
    uploaded_file = request.FILES['file']
    file_path = os.path.join(settings.TEMP_UPLOAD_DIR, uploaded_file.name)

    with open(file_path, 'wb') as file:
        for chunk in uploaded_file.chunks():
            file.write(chunk)

    def perform_processing():
        test = Resumee(
            path=file_path,
            token=token
        )
        print('[+] NER Results:', test.ner)
        print('[+] Information-Extraction Results:', test.information)
        print('[+] Person-info Results:', test.person_info)

        test_job = Jobs('../data/岗位要求.docx')
        print(test.fit(test_job.job_info))

        record = Applicant.objects.create(ner=test.ner,
                                          information=test.information,
                                          event=test.person_info,
                                          match=test.fit(test_job.job_info))

        return JsonResponse({'ret': 0, 'id': record.id})

    def send_response():
        return JsonResponse({'ret': 0, 'id': 666})

    # 创建并启动线程
    processing_thread = threading.Thread(target=perform_processing)
    processing_thread.start()

    # 在当前线程中返回 JsonResponse
    response = send_response()

    # 等待处理线程完成
    processing_thread.join()

    return response
