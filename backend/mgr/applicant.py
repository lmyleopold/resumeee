"""
    >File Name: applicant
    >Author: lmyleopold
    >Created Time: 2023/5/22 23:16
"""
from django.http import JsonResponse
import json
from common.models import Applicant
from django.core.paginator import Paginator, EmptyPage


def dispatcher(request):  # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # 根据session判断用户是否是登录的管理员用户
    # if 'usertype' not in request.session:
    #     return JsonResponse({
    #         'ret': 302,
    #         'msg': '未登录',
    #         'redirect': '/mgr/sign.html'},
    #         status=302)
    #
    # if request.session['usertype'] != 'mgr':
    #     return JsonResponse({
    #         'ret': 302,
    #         'msg': '用户非mgr类型',
    #         'redirect': '/mgr/sign.html'},
    #         status=302)

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
    # 增加对分页的支持
    try:
        # 要获取的第几页
        pagenum = request.params['pagenum']
        # 每页要显示多少条记录
        pagesize = request.params['pagesize']
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        qs = Applicant.objects.values()

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


def addapplicant(request):
    info = request.params['data']
    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    # record = Applicant.objects.create(name=info['name'],
    #                                  phonenumber=info['phonenumber'],
    #                                  job=info['job'])
    record = Applicant.objects.create(ner=info['ner'],
                                     information=info['information'],
                                     event=info['event'])
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

    if 'ner' in newdata:
        applicant.ner = newdata['ner']
    if 'information' in newdata:
        applicant.information = newdata['information']
    if 'event' in newdata:
        applicant.address = newdata['event']
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
