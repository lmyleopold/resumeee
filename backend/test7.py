"""
    >File Name: test7
    >Author: lmyleopold
    >Created Time: 2023/7/2 23:37
"""
import requests
import mysql.connector


def check(reponse2):
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
    data = response2.json()
    assert data['id'] == db_data[-1][0]
    assert data['ret'] == 0
    return

# 先登陆,获取 sessionid
payload = {'username': 'lmy', 'password': '88888888'}
response = requests.post("http://localhost/api/mgr/signin", data=payload)
sessionid = response.cookies['sessionid']
payload2 = {
    'action': 'add_applicant',
    'data': {
        'name': '王燊超',
        'phonenumber': '13345679934',
        'job': '后卫'
    }
}
response2 = requests.post('http://localhost/api/mgr/applicants',
              json=payload2,
              cookies={'sessionid': sessionid})

check(response2)
# 添加结果
print('添加正确')
