"""
    >File Name: test6
    >Author: lmyleopold
    >Created Time: 2023/7/2 22:48
"""
import requests
import mysql.connector


def getApplicant():
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
    query = "SELECT * FROM common_applicant"
    cursor.execute(query)
    # 获取数据库查询结果
    db_data = cursor.fetchall()
    # 关闭数据库连接
    cursor.close()
    cnx.close()
    # print(db_data)
    # [(1, '武磊', '13886666666', '前锋'), (2, '颜骏凌', '13995555555', '门将'), (3, '奥斯卡', '13345679934', '中场')]
    return db_data


def check(response1, db_data1, payload1):
    # 检查状态码是否为200
    assert response1.status_code == 200
    # 检查响应内容是否为JSON格式
    assert response1.headers.get('Content-Type') == 'application/json'
    # 获取JSON响应体并进行断言
    data = response1.json()
    assert data['ret'] == 0
    assert len(data['retlist']) == payload1['pagenum']*payload1['pagesize']
    # 比较数据库查询结果与返回结果
    for i in range(len(data['retlist'])):
        assert db_data1[i] == tuple(data['retlist'][i].values())
    # assert data['retlist'] == [{'id': 1, 'job': '前锋', 'name': '武磊', 'phonenumber': '13886666666'},
    #                            {'id': 2, 'job': '门将', 'name': '颜骏凌', 'phonenumber': '13995555555'}]
    assert data['total'] == len(db_data1)


# 先登陆,获取 sessionid
payload = {'username': 'lmy', 'password': '88888888'}
response = requests.post("http://localhost/api/mgr/signin", data=payload)
sessionid = response.cookies['sessionid']
# 再发送列出请求，注意多了 pagenum 和 pagesize
payload1 = {
    'action': 'list_applicant',
    'pagenum': 1,
    'pagesize': 2
}
response1 = requests.get('http://localhost/api/mgr/applicants',
              params=payload1,
              cookies={'sessionid': sessionid})

db_data1 = getApplicant()
check(response1, db_data1, payload1)
# 打印结果
print("返回正确")
