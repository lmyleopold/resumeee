# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from common.models import Job
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage


def applicant(request):
    return HttpResponse("这里是申请者所看到的界面")


def resume(request):
    return HttpResponse("这里提交和查看已提交简历")


# HTML模板
html_template = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
table {
    border-collapse: collapse;
}
th, td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}
</style>
</head>
    <body>
        <table>
        <tr>
        <th>id</th>
        <th>岗位</th>
        <th>工作描述</th>
        </tr>

        %s


        </table>
    </body>
</html>
'''


def listjobs(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # 每条表记录都是是一个dict对象，
    # key 是字段名，value 是 字段值
    qs = Job.objects.values()
    # 检查url中是否有参数name
    name = request.GET.get('name', None)
    # 如果有，添加过滤条件
    if name:
        qs = qs.filter(name=name)

    # 方式一：按字符串返回
    # retStr = ''
    # for job in qs:
    #     for name, value in job.items():
    #         retStr += f'{name} : {value} | '
    #
    #     # <br> 表示换行
    #     retStr += '<br>'

    # 方式二：按简单HTML返回
    tableContent = ''
    for job in qs:
        tableContent += '<tr>'

        for name, value in job.items():
            tableContent += f'<td>{value}</td>'

        tableContent += '</tr>'

    return HttpResponse(html_template % tableContent)

def jobs(request):
    try:
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        qs = Job.objects.values()
        # 要获取的第几页
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
        return HttpResponse("这里是分页展示岗位")
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})
