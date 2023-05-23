登录 /login POST `再说吧`

角色 applicant

- applicant 提交 /resume POST `文件、userid` 200 简历号(hash) OK    ERROR
- 获取简历状态 /resume GET `简历号、userid` 200 表单 OK    ERROR
- 获取所有工作描述 /jobs/<page> `筛选条件` GET 200 列表 OK    ERROR

角色 mgr

- 批量提交 /resume POST `文件、userid` 200 简历号(hash) OK    ERROR

- 获取所有简历描述 /resume/<page> `筛选条件` GET 200 列表 OK    ERROR

- 获取对某一工作的申请者 /jobs/apply

  

## 登录系统

### 请求消息

```py
POST  /api/mgr/signin  HTTP/1.1
Content-Type:   application/x-www-form-urlencoded
```

### 请求参数

http 请求消息 body 中 参数以 格式 x-www-form-urlencoded 存储

需要携带如下参数，

- username

  用户名

- password

  密码

### 响应消息

```py
HTTP/1.1 200 OK
Content-Type: application/json
```

### 响应内容

http 响应消息 body 中， 数据以json格式存储，

如果登录成功，返回如下

```json
{
    "ret": 0
}
```

ret 为 0 表示登录成功

如果登录失败，返回失败的原因，示例如下

```json
{
    "ret": 1,    
    "msg":  "用户名或者密码错误"
}
```

ret 不为 0 表示登录失败， msg字段描述登录失败的原因



## 申请者数据

### 列出所有申请者

#### 请求消息

```py
GET  /api/mgr/applicants?action=list_applicant  HTTP/1.1
```

#### 请求参数

http 请求消息 url 中 需要携带如下参数，

- action

  填写值为 list_applicant

#### 响应消息

```py
HTTP/1.1 200 OK
Content-Type: application/json
```

#### 响应内容

http 响应消息 body 中， 数据以json格式存储，

如果获取信息成功，返回如下

```json
{
    "ret": 0,
    "retlist": [
        {
            "id": 1,
            "name": "武磊",
            "phonenumber": "13886666666",
            "job": "前锋",
            # more to add
        },
        
        {
            "id": 2,
            "name": "颜骏凌",
            "phonenumber": "13995555555",
            "job": "门将"，
            # more to add
        }
    ]              
}
```

ret 为 0 表示登录成功

retlist 里面包含了所有的申请者信息列表。

每个申请者信息以如下格式存储

```json
{
   "id": 1,
    "name": "武磊",
    "phonenumber": "13886666666",
    "job": "前锋",
    # more to add
}
```



### 添加一个申请者

#### 请求消息

```py
POST  /api/mgr/applicants  HTTP/1.1
Content-Type:   application/json
```

#### 请求参数

http 请求消息 body 携带添加申请者的信息

消息体的格式是json，如下示例：

```json
{
    "action":"add_applicant",
    "data":{
        "name":"王燊超",
        "phonenumber":"13345679934",
        "job":"后卫",
    }
}
```

其中

`action` 字段固定填写 `add_applicant` 表示添加一个申请者

`data` 字段中存储了要添加的申请者的信息

服务端接受到该请求后，应该在系统中增加一位这样的申请者。

#### 响应消息

```py
HTTP/1.1 200 OK
Content-Type: application/json
```

#### 响应内容

http 响应消息 body 中， 数据以json格式存储，

如果添加成功，返回如下

```json
{
    "ret": 0,
    "id" : 6
}
```

ret 为 0 表示成功。

id 为 添加申请者的id号。

如果添加失败，返回失败的原因，示例如下

```json
{
    "ret": 1,    
    "msg": "客户名已经存在"
}
```

ret 不为 0 表示失败， msg字段描述添加失败的原因



### 修改申请者信息

#### 请求消息

```py
PUT  /api/mgr/applicants  HTTP/1.1
Content-Type:   application/json
```

#### 请求参数

http 请求消息 body 携带修改申请者的信息

消息体的格式是json，如下示例：

```json
{
    "action":"modify_applicant",
    "id": 6,
    "newdata":{
        "name":"蔡慧康",
        "phonenumber":"13345678888",
        "job":"中场"
    }
}
```

其中

`action` 字段固定填写 `modify_applicant` 表示修改一个申请者的信息

`id` 字段为要修改的客户的id号

`newdata` 字段中存储了修改后的申请者的信息

服务端接受到该请求后，应该在系统中增加一位这样的申请者。

#### 响应消息

```py
HTTP/1.1 200 OK
Content-Type: application/json
```

#### 响应内容

http 响应消息 body 中， 数据以json格式存储，

如果修改成功，返回如下

```json
{
    "ret": 0
}
```

ret 为 0 表示成功。

如果修改失败，返回失败的原因，示例如下

```json
{
    "ret": 1,    
    "msg": "申请者已经存在"
}
```

ret 不为 0 表示失败， msg字段描述添加失败的原因



### 删除申请者信息

#### 请求消息

```py
DELETE  /api/mgr/applicants  HTTP/1.1
Content-Type:   application/json
```

#### 请求参数

http 请求消息 body 携带要删除客户的id

消息体的格式是json，如下示例：

```json
{
    "action":"del_applicant",
    "id": 6
}
```

其中

`action` 字段固定填写 `del_applicant` 表示删除一个申请者

`id` 字段为要删除的申请者的id号

服务端接受到该请求后，应该在系统中尝试删除该id对应的申请者。

#### 响应消息

```py
HTTP/1.1 200 OK
Content-Type: application/json
```

#### 响应内容

http 响应消息 body 中， 数据以json格式存储，

如果删除成功，返回如下

```json
{
    "ret": 0
}
```

ret 为 0 表示成功。

如果删除失败，返回失败的原因，示例如下

```json
{
    "ret": 1,    
    "msg": "id为 6 的申请者不存在"
}
```

ret 不为 0 表示失败， msg字段描述添加失败的原因





## 岗位数据

### 列出所有岗位

#### 请求消息

```py
GET  /api/mgr/jobs  HTTP/1.1
GET  /applicant/jobs  HTTP/1.1
```

#### 请求参数

http 请求消息 url 中 需要携带如下参数，

- action

  填写值为 list_job

#### 响应消息

```py
HTTP/1.1 200 OK
Content-Type: application/json
```

#### 响应内容

http 响应消息 body 中， 数据以json格式存储，

如果获取信息成功，返回如下

```json
{
    "ret": 0,
    "retlist": [
        {"id": 1, "name": "前锋",  "desc": "射门"},
        {"id": 2, "name": "门将",  "desc": "守门"}
    ]              
}
```

ret 为 0 表示登录成功

retlist 里面包含了所有的岗位信息列表。

每个岗位信息以如下格式存储

```json
    {"id": 1, "name": "前锋",  "desc": "射门"}
```



### 添加一个岗位

#### 请求消息

```py
POST  /api/mgr/jobs  HTTP/1.1
Content-Type:   application/json
```

#### 请求参数

http 请求消息 body 携带添加岗位的信息

消息体的格式是json，如下示例：

```json
{
    "action":"add_job",
    "data":{
        "name": "后卫",
        "desc": "防守",
    }
}
```

其中

`action` 字段固定填写 `add_job` 表示添加一个药品

`data` 字段中存储了要添加的药品的信息

服务端接受到该请求后，应该在系统中增加这样的药品。

#### 响应消息

```py
HTTP/1.1 200 OK
Content-Type: application/json
```

#### 响应内容

http 响应消息 body 中， 数据以json格式存储，

如果添加成功，返回如下

```json
{
    "ret": 0,
    "id" : 6
}
```

ret 为 0 表示成功。

id 为 添加岗位的id号。

如果添加失败，返回失败的原因，示例如下

```json
{
    "ret": 1,    
    "msg": "岗位已经存在"
}
```

ret 不为 0 表示失败， msg字段描述添加失败的原因



### 修改岗位信息

#### 请求消息

```py
PUT  /api/mgr/jobs  HTTP/1.1
Content-Type:   application/json
```

#### 请求参数

http 请求消息 body 携带修改岗位的信息

消息体的格式是json，如下示例：

```json
{
    "action":"modify_job",
    "id": 6,
    "newdata":{
        "name": "中场",
        "desc": "拦截；向前输送",
    }
}
```

其中

`action` 字段固定填写 `modify_job` 表示修改一个岗位的信息

`id` 字段为要修改的岗位的id号

`newdata` 字段中存储了修改后的岗位的信息

服务端接受到该请求后，应该在系统中增加一位这样的岗位。

#### 响应消息

```py
HTTP/1.1 200 OK
Content-Type: application/json
```

#### 响应内容

http 响应消息 body 中， 数据以json格式存储，

如果修改成功，返回如下

```json
{
    "ret": 0
}
```

ret 为 0 表示成功。

如果修改失败，返回失败的原因，示例如下

```json
{
    "ret": 1,    
    "msg": "岗位不存在"
}
```

ret 不为 0 表示失败， msg字段描述添加失败的原因



### 删除岗位信息

#### 请求消息

```py
DELETE  /api/mgr/jobs  HTTP/1.1
Content-Type:   application/json
```

#### 请求参数

http 请求消息 body 携带要删除岗位的id

消息体的格式是json，如下示例：

```json
{
    "action":"del_job",
    "id": 6
}
```

其中

`action` 字段固定填写 `del_job` 表示删除一个药品

`id` 字段为要删除的岗位的id号

服务端接受到该请求后，应该在系统中尝试删除该id对应的岗位。

#### 响应消息

```py
HTTP/1.1 200 OK
Content-Type: application/json
```

#### 响应内容

http 响应消息 body 中， 数据以json格式存储，

如果删除成功，返回如下

```json
{
    "ret": 0
}
```

ret 为 0 表示成功。

如果删除失败，返回失败的原因，示例如下

```json
{
    "ret": 1,    
    "msg": "id为 6 的岗位不存在"
}
```

ret 不为 0 表示失败， msg字段描述添加失败的原因