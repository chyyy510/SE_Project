# SE_Project

## 后端的运行

需要安装 MySQL，创建 `pku_backend` 数据库。在项目根目录创建 `.env` 文件写入数据库密码。

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

### Windows

```bash
pip install pycryptodomex django djangorestframework djangorestframework-simplejwt django-cors-headers Pillow python-decouple mysqlclient
```

```bash
python manage.py runserver 0.0.0.0:8000
```

### Linux（仅在 Ubuntu 24.04 测试）

在你的**虚拟环境**中：

```bash
pip install pycryptodomex django djangorestframework djangorestframework-simplejwt django-cors-headers Pillow python-decouple pymysql
```

如果没有 `pip`，可以 `sudo apt install python3-pip` 安装。然后 `sudo apt install python<版本>-venv` 安装 `venv`（`<版本>` 替换为 Python 版本，对于 Ubuntu 24.04 来说是 3.12）。

创建虚拟环境，`<虚拟环境路径>` 替换为你想要的路径。一般情况下是 `.venv`：

```bash
python3 -m venv <虚拟环境路径>
```

接下来激活虚拟环境，如果你用 bash/zsh 可以：

```bash
source .venv/bin/activate
```

最后：


```bash
python3 manage.py runserver 0.0.0.0:8000
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

[http://backend-ip:8000/users/\<int:pk\>/]()

GET 获取id为pk的用户详细信息(id是数据库自动生成的，不同于开发者分配的uid)

status_code=200
```json
{
    "email": "123456@qq.com",
    "id": 1,
    "is_active": true,
    "is_staff": false,
    "message": "Find the user successfully. 成功找到该用户。",
    "password": "4d28edb601106a84742a3c1a394db573d5c8bf2bdc86c36a3652bdad67c7db11",
    "uid": 1000001,
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
    "message": "Access token has been refreshed.access令牌已更新。"
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

status_code=200

```json
{
    "creator": 1,
    "description": "This is a test experiment.",
    "id": 1,
    "message": "Find the experiment successfully. 成功找到该实验。",
    "money_left": "0.00",
    "money_paid": "0.00",
    "money_per_person": "10.00",
    "person_already": 0,
    "person_wanted": 20,
    "status": "open",
    "time_created": "2024-11-13T15:52:50.431072+08:00",
    "time_modified": "2024-11-13T15:52:50.431078+08:00",
    "title": "test_exp"
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
}
```

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
    "title": "another_test_exp"
}
```

#### experiment-search

[http://backend-ip:8000/experiments/search/?title=aaa&description=bbb&orderby=ccc&sort=ddd]()

GET 查找title中包含aaa且description中包含bbb且按ccc字段降序或升序排列的实验列表

四个关键字可部分使用，title默认为空，description默认为空（即包含全部实验），orderby默认按id，sort可选asc或desc，默认为asc。

后端返回满足搜索条件的实验列表

status_code=200
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
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
            "title": "another_test_exp"
        },
        {
            "creator": 1,
            "description": "This is another test experiment.",
            "id": 7,
            "money_left": "0.00",
            "money_paid": "0.00",
            "money_per_person": "10.00",
            "person_already": 0,
            "person_wanted": 20,
            "status": "open",
            "time_created": "2024-11-13T21:27:06.787422+08:00",
            "time_modified": "2024-11-13T21:27:06.787444+08:00",
            "title": "another_test_exp"
        }
    ]
}
```

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