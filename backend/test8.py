"""
    >File Name: test8
    >Author: lmyleopold
    >Created Time: 2023/7/2 23:56
"""
import requests
import mysql.connector


def getJob():
    # 连接到MySQL数据库
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='resumeee'
    )
    # 创建游标对象
    cursor = cnx.cursor()
    # 执行数据库查询
    query = "SELECT * FROM common_job"
    cursor.execute(query)
    # 获取数据库查询结果
    db_data = cursor.fetchall()
    # 关闭数据库连接
    cursor.close()
    cnx.close()
    return db_data


def check(response, db_data, payload):
    # 检查状态码是否为200
    assert response.status_code == 200
    # 检查响应内容是否为JSON格式
    assert response.headers.get('Content-Type') == 'application/json'
    # 获取JSON响应体并进行断言
    data = response.json()
    assert data['ret'] == 0
    assert len(data['retlist']) == payload['pagenum']*payload['pagesize']
    # 比较数据库查询结果与返回结果
    for i in range(len(data['retlist'])):
        assert db_data[i] == tuple(data['retlist'][i].values())
    assert data['total'] == len(db_data)


def mgr_test():
    # 先登陆,获取 sessionid
    payload = {'username': 'lmy', 'password': '88888888'}
    response = requests.post("http://localhost/api/mgr/signin", data=payload)
    sessionid = response.cookies['sessionid']
    # 再发送列出请求，注意多了 pagenum 和 pagesize
    payload3 = {
        'action': 'list_job',
        'pagenum': 1,
        'pagesize': 2
    }
    response3 = requests.get('http://localhost/api/mgr/jobs',
                            params=payload3,
                            cookies={'sessionid': sessionid})

    db_data3 = getJob()
    check(response3, db_data3, payload3)
    # 打印结果
    print("返回正确")


def applicant_test():
    # 先登陆,获取 sessionid
    payload = {'username': 'test', 'password': '123456'}
    response = requests.post("http://localhost/applicant/signin", data=payload)
    sessionid = response.cookies['sessionid']
    # 再发送列出请求，注意多了 pagenum 和 pagesize
    payload4 = {
        'action': 'list_job',
        'pagenum': 1,
        'pagesize': 2
    }
    response4 = requests.get('http://localhost/applicant/jobs/',
                            params=payload4,
                            cookies={'sessionid': sessionid})
    db_data4 = getJob()
    check(response4, db_data4, payload4)
    # 打印结果
    print("返回正确")


mgr_test()
applicant_test()
