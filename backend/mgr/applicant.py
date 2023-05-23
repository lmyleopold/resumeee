"""
    >File Name: applicant
    >Author: lmyleopold
    >Created Time: 2023/5/22 23:16
"""
from django.http import JsonResponse
import json
from common.models import Applicant

def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_applicant':
        return listapplicants(request)
    elif action == 'add_applicant':
        return addapplicant(request)
    elif action == 'modify_applicant':
        return modifyapplicant(request)
    elif action == 'del_applicant':
        return deleteapplicant(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def listapplicants(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Applicant.objects.values()
    # 将 QuerySet 对象 转化为 list 类型，否则不能 被 转化为 JSON 字符串
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retlist': retlist})


def addapplicant(request):
    info = request.params['data']
    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = Applicant.objects.create(name=info['name'],
                                     phonenumber=info['phonenumber'],
                                     job=info['job'])
    return JsonResponse({'ret': 0, 'id': record.id})


def modifyapplicant(request):
    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作
    applicantid = request.params['id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        applicant = Applicant.objects.get(id=applicantid)
    except Applicant.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{applicantid}`的申请者不存在'
        }

    if 'name' in newdata:
        applicant.name = newdata['name']
    if 'phonenumber' in newdata:
        applicant.phonenumber = newdata['phonenumber']
    if 'job' in newdata:
        applicant.address = newdata['job']
    # 将修改信息保存到数据库
    applicant.save()
    return JsonResponse({'ret': 0})


def deleteapplicant(request):
    applicantid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        applicant = Applicant.objects.get(id=applicantid)
    except Applicant.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{applicantid}`的申请者不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    applicant.delete()
    return JsonResponse({'ret': 0})
