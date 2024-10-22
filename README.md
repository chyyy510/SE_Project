# SE_Project

## 数据传输标准

### User

- user-list: [http://backend-ip:8000/users/]() GET 获取当前所有用户的信息列表
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "Alice@gmail.com",
            "is_active": true,
            "is_staff": false,
            "nickname": "Alice",
            "password_hashed": "wevn852",
            "uid": 46531
        },
        {
            "email": "Bob@stu.pku.edu.cn",
            "is_active": true,
            "is_staff": false,
            "nickname": "Bob",
            "password_hashed": "ghio63",
            "uid": 435856
        }
    ]
}
```

- user-detail: [http://backend-ip:8000/users/\<int:pk\>]() GET 获取id为pk的用户详细信息(id是数据库自动生成的，不同于开发者分配的uid)
```json
{
    "email": "Alice@gmail.com",
    "is_active": true,
    "is_staff": false,
    "nickname": "Alice",
    "password_hashed": "wevn852",
    "uid": 46531
}
```

- user-register: [http://backend-ip:8000/users/register/]() POST 向后端提交注册信息 TODO:暂定只需传递以下字段
```json
{
    "email": "Alice@gmail.com",
    "nickname": "Alice",
    "password_hashed": "wevn852",
}
```
- user-login: [http://backend-ip:8000/users/login/] POST 向后端提交登录信息 TODO:暂定只需传递以下字段
```json
{
    "email": "Alice@gmail.com",
    "password_hashed": "wevn852",
}

```