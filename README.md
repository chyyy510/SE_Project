# SE_Project

## 后端的运行

### 配置文件

需要安装 MySQL，创建 `pku_backend` 数据库。在项目根目录创建 `.env` 文件写入数据库密码。`.env` 的示例如下：

```ini
DATABASE_NAME=pku_backend
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
DATABASE_PASSWORD=123456
DATABASE_USERNAME=root
PRIVATE_KEY_PATH=<path to private key>
LOGFILE_PATH=<path to log>
```

如果你不想安装 MySQL 可以直接连接至校园网内的测试数据库。在 `backend/backend/settings.py` 修改：

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "<在群里问>（x",
        "USER": "<在群里问>",
        "PASSWORD": "<在群里问>",
        "HOST": "<在群里问>",
        "PORT": "<在群里问>",
    }
}
```

### 依赖项的安装

#### 除了 `mysqlclient` 的所有依赖项：

```bash
pip install pycryptodomex django djangorestframework djangorestframework-simplejwt django-cors-headers Pillow python-decouple
```

如果你使用 Linux（仅在 Ubuntu 24.04 测试），建议使用虚拟环境：

```bash
sudo apt install python3-pip python3.12-venv
python3 -m venv .venv
source .venv/bin/activate # 假设使用 bash/zsh
```

#### 安装 `mysqlclient`

首先尝试：

```bash
pip install mysqlclient
```
如果安装失败，则请见下方的从源代码构建 `mysqlclient` 指南。

##### Windows

1. 安装 `https://mariadb.com/downloads/connectors/`
2. 设置 `MYSQLCLIENT_CONNECTOR`。如果你安装的是 64 位版本 MariaDB C Connector，且使用 PowerShell：

```pwsh
$env:MYSQLCLIENT_CONNECTOR='C:\Program Files\MariaDB\MariaDB Connector C 64-bit\'
```

此时再尝试：

```bash
pip install mysqlclient
```

##### Linux（仅在 Ubuntu 24.04 测试）

```bash
sudo apt install pkg-config python3-dev default-libmysqlclient-dev build-essential libssl-dev
export MYSQLCLIENT_CFLAGS=$(mysql_config --cflags)
export MYSQLCLIENT_LDFLAGS=$(mysql_config --libs)
pip install mysqlclient
```

### 启动服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

## 数据传输标准

返回的详细信息，如果出错则统一为detail，正常则统一为message。

### User

#### user-list

[http://backend-ip:8000/users/]()

GET 获取当前所有用户的信息列表

status_code=200
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "123456@qq.com",
            "id": 1,
            "is_active": true,
            "is_staff": false,
            "password": "4d28edb601106a84742a3c1a394db573d5c8bf2bdc86c36a3652bdad67c7db11",
            "uid": 1000001,
            "username": "123456"
        },
        {
             "email": "test@qq.con",
            "id": 2,
            "is_active": true,
            "is_staff": false,
            "password": "1015c01afd731ee9494902a36d98aca8615f37a695a1ce7e99627c37ba015c85",
            "uid": 1000002,
            "username": "test"
        }
    ]
}
```

#### user-detail

[http://backend-ip:8000/users/detail/?username=xxx]()

GET 获取username为xxx的用户详细信息
- avatar: 头像url

status_code=200
```json
{
    "avatar": "/media/avatar/user_0/default_avatar.png",
    "email": "123456@qq.com",
    "introduction": "Nothing here.",
    "message": "Find the user successfully. 成功找到该用户。",
    "nickname": "user1000002",
    "point": 0,
    "username": "123456"
}
```

若该用户不存在，则返回

status_code=404
```json
{
    "detail": "User doesn't exist. 该用户不存在。"
}
```

#### user-register

[http://backend-ip:8000/users/register/]()

POST 向后端提交注册信息 TODO:暂定只需传递以下字段
```json
{
    "email": "Alice@gmail.com",
    "username": "Alice",
    "password_encrypted": "wevn852",
}
```

若数据库中已有email或username，返回错误

status_code=400
```json
{
    "detail": "Email already exists.邮箱已存在。"
}
```
或
```json
{
    "detail": "Username already exists.用户名已存在。"
}
```

成功注册则返回

status_code=200
```json
{
    "email": "Alice@gmail.com",
    "id": 9,
    "is_active": true,
    "is_staff": false,
    "password": "de06629acd0fcd41f25333870f8749fbfacad8f78ee10603aa6c0c9d1f370676",
    "uid": 1000008,
    "username": "Alice"
}
```

#### user-login

[http://backend-ip:8000/users/login/]()

POST 向后端提交登录信息 TODO:暂定只需传递以下字段
```json
{
    "email": "Alice@gmail.com",
    "password_encrypted": "wevn852",
}
```

登录成功后端返回

status_code=200
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5NzQ3NTc2LCJpYXQiOjE3Mjk3NDcyNzYsImp0aSI6ImJhMWRhOTMyMWJmYjQyOWVhZTJiNDBmOGFhOTdhZDY2IiwidXNlcl9pZCI6MX0.YKAtBt7fAzr8Q8cenyrJfrCAuMWb41co22okeZ1zuoo",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyOTgzMzY3NiwiaWF0IjoxNzI5NzQ3Mjc2LCJqdGkiOiI3YjdmYzc4YzU1MTc0ODUzOGY1ZGFmMDA2MTk0Y2ExYyIsInVzZXJfaWQiOjF9.TWVHrAkGZlQFEhEGgENiA_V75Fh_EVRcr1kdAiusF_0",
    "user": {
        "email": "Alice@gmail.com",
        "is_active": true,
        "username": "Alice"
    }
}
```
登录失败后端返回

status_code=400
```json
{
    "detail": "Invalid email.邮箱不存在。"
}
```
或
```json
{
    "detail": "Invalid password.密码错误。"
}
```

#### token-refresh

[http://backend-ip:8000/users/token/refresh/]()

POST 向后端提交之前获取的refresh

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyOTgzMzY3NiwiaWF0IjoxNzI5NzQ3Mjc2LCJqdGkiOiI3YjdmYzc4YzU1MTc0ODUzOGY1ZGFmMDA2MTk0Y2ExYyIsInVzZXJfaWQiOjF9.TWVHrAkGZlQFEhEGgENiA_V75Fh_EVRcr1kdAiusF_0"
}
```

后端返回更新后的access

status_code=200
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0MTg4Njg2LCJpYXQiOjE3MzQxODY4MjYsImp0aSI6IjQ5ZTY2MmI2MTI1ODQxMDliYzU3ZGE3OWU3NjE3ZDZkIiwidXNlcl9pZCI6MX0.ftsZ8dpZ6028bRY_FqtBOt1c8BF-B0WR4sBvMXOp6sI",
    "message": "Access token has been refreshed. access令牌已更新。"
}
```

若refresh错误，后端返回

status_code=401
```json
{
    "detail": "Token is invalid or expired.令牌无效或已过期。"
}
```

#### user-profile

[http://backend-ip:8000/users/profile/]()

GET 前端获取当前登录用户的主页信息TODO:

需要在header中包含**Authorization:"Bearer \<之前获取的access\>"**（没有尖括号）

### experiment

#### experiment-list

[http://backend-ip:8000/experiments/]()

GET 前端获取所有的实验信息

```json
{
    "count": 7,
    "next": null,
    "previous": null,
    "results": [
        {
            "creator": 1,
            "description": "This is a test experiment.",
            "id": 1,
            "money_left": "0.00",
            "money_paid": "0.00",
            "money_per_person": "10.00",
            "person_already": 0,
            "person_wanted": 20,
            "status": "open",
            "time_created": "2024-11-13T15:52:50.431072+08:00",
            "time_modified": "2024-11-13T15:52:50.431078+08:00",
            "title": "test_exp"
        },
        {
            "creator": 1,
            "description": "This is a test experiment.",
            "id": 2,
            "money_left": "0.00",
            "money_paid": "0.00",
            "money_per_person": "10.00",
            "person_already": 0,
            "person_wanted": 20,
            "status": "open",
            "time_created": "2024-11-13T16:20:06.554001+08:00",
            "time_modified": "2024-11-13T16:20:06.554006+08:00",
            "title": "test_exp"
        },
        ...
    ]
}
```

#### experiment-detail

[http://backend-ip:8000/experiments/\<int:pk\>/]()

GET 获取id为pk的实验详细信息

headers中包含Authorization，用于判断relationship
- relationship取值
  - 未登录：unauthorized
  - 创建者：creator
  - 已申请者：applicant
  - 非创建也未申请：passer-by
- creator
  - 现在返回的是用户的username

status_code=200
```json
{
    "activity_location": "家四",
    "activity_time": "2024-12-16",
    "creator": "abc",
    "description": "hhh",
    "id": 1,
    "message": "Find the experiment successfully. 成功找到该实验。",
    "money_left": "0.00",
    "money_paid": "0.00",
    "money_per_person": "0.00",
    "person_already": 0,
    "person_wanted": 4,
    "relationship": "applicant",
    "status": "open",
    "time_created": "2024-12-16T15:46:00.454790+08:00",
    "time_modified": "2024-12-16T15:46:00.454868+08:00",
    "title": "test1"
}
```

#### experiment-create

[http://backend-ip:8000/experiments/create/]()

POST 前端向后端发送要创建的实验信息，进行此功能必须先登录

前端发送：
```json
{
    "title": "xxx",
    "description": "xxx",
    "person_wanted": 20,
    "money_per_person": 10,
    "tags": 13,
    "activity_time": "2024-01-01",
    "activity_location": "北京大学",
}
```

> 这里，15 = 0b1101，意为该实验包含 id 为 1、3、4 的 tag。

后端返回创建后的详细信息：

status_code=200
```json
{
    "creator": 1,
    "description": "This is another test experiment.",
    "id": 8,
    "money_left": "0.00",
    "money_paid": "0.00",
    "money_per_person": "10.00",
    "person_already": 0,
    "person_wanted": 20,
    "status": "open",
    "time_created": "2024-11-13T22:22:54.415083+08:00",
    "time_modified": "2024-11-13T22:22:54.415104+08:00",
    "title": "another_test_exp",
    "activity_time": "2024-01-01",
    "activity_location": "北京大学",
}
```

#### experiment-search

[http://backend-ip:8000/experiments/search/?keyword=bbb&orderby=ccc&sort=ddd]()

GET 查找keyword中包含bbb且按ccc字段降序或升序排列的实验列表

三个关键字可部分使用，keyword默认为空（即包含全部实验），orderby默认按id，sort可选asc或desc，默认为asc。

后端返回满足搜索条件的实验列表

status_code=200
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "activity_location": "家四",
            "activity_time": "2024-12-16",
            "creator": 1,
            "description": "hhh",
            "id": 1,
            "money_left": "0.00",
            "money_paid": "0.00",
            "money_per_person": "0.00",
            "person_already": 0,
            "person_wanted": 4,
            "status": "open",
            "time_created": "2024-12-16T15:46:00.454790+08:00",
            "time_modified": "2024-12-16T15:46:00.454868+08:00",
            "title": "test1"
        },
        ...
    ]
}
```

#### experiment-create-search

[http://127.0.0.1:8000/experiments/create/search/?keyword=aaa&orderby=bbb&sort=ccc]()

### engagement

#### experiment-engage

[http://backend-ip:8000/relations/engage/]()

POST

#### experiment-engage-search

[http://backend-ip:8000/relations/engage/search/?keyword=aaa&orderby=bbb&sort=ccc]()

### qualification

#### qualify-volunteer

[http://backend-ip:8000/relations/qualify/volunteers/]()

### volunteer-list

[http://backend-ip:8000/relations/volunteers/list/?experiment=xxx]()




### other

所有需要登录进行的操作，若未登录或token过期，均返回401_UNAUTHORIZED错误，其中

若未登录

status_code=401
```json
{
    "detail": "Authentication required. 该功能需要先登录。"
}
```

若令牌无效或过期

status_code=401
```json
{
    "code": "token_not_valid",
    "detail": "此令牌对任何类型的令牌无效",
    "messages": [
        {
            "message": "令牌无效或已过期",
            "token_class": "AccessToken",
            "token_type": "access"
        }
    ]
}
```

refresh token过期:
```json
{
    "code": "token_not_valid",
    "detail": "令牌无效或已过期"
}
```

### 所有 tag：

- API：`<host>:<port>/relations/tags/`
- 方法：GET
- 返回
```json
[
    {
        "name": "tag1"
    },
    {
        "name": "tag2"
    }
]
```

### 用户信息的更新：

- API：`<host>:<port>/users/profile/edit/`
- 方法：POST
- 请求体：
  ```json
  {
      "email": "alice@gmail.com",
      "username": "alice",
      "old_password_encrypted": "",
      "new_password_encrypted": ""
  }
  ```
  以上字段不必同时存在。例如，如果只更新密码：
  ```json
  {
      "old_password_encrypted": "",
      "new_password_encrypted": ""
  }
  ```
  只更新email：
  ```json
  { "email": "alice@gmail.com"  }
  ```

### 实验信息更新

- API：`<host>:<port>/experiments/edit/`
- 方法：POST
- 请求体：
  ```json
  {
      "id": 1,
      "title": "Exp 1",
      "description": "desc 1",
      "person_wanted": 1,
      "money_per_person": 1,
      "activity_time": "",
      "activity_location": ""
  }
  ```
  除 id 外，以上字段不必同时存在。如果只更新标题：
  ```json
  {
    "id": 1,
    "title": "Exp 1"
  }
  ```
