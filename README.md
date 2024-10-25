# SE_Project

## 数据传输标准

### User

#### user-list

[http://backend-ip:8000/users/]() 

GET 获取当前所有用户的信息列表
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

#### user-detail

[http://backend-ip:8000/users/\<int:pk\>]() 

GET 获取id为pk的用户详细信息(id是数据库自动生成的，不同于开发者分配的uid)
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
```json
{
    "message": "Email already exists."
}
```
或
```json
{
    "message": "Username already exists."
}
```
#### user-login

[http://backend-ip:8000/users/login/] 

POST 向后端提交登录信息 TODO:暂定只需传递以下字段
```json
{
    "email": "Alice@gmail.com",
    "password_encrypted": "wevn852",
}
```

登录成功后端返回

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
```json
{
    "error": "Invalid email"
}
```
或
```json
{
    "error": "Invalid password"
}
```

#### token-refresh

[http://backend-ip:8000/users/token/refresh/]

POST 向后端提交之前获取的refresh

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyOTgzMzY3NiwiaWF0IjoxNzI5NzQ3Mjc2LCJqdGkiOiI3YjdmYzc4YzU1MTc0ODUzOGY1ZGFmMDA2MTk0Y2ExYyIsInVzZXJfaWQiOjF9.TWVHrAkGZlQFEhEGgENiA_V75Fh_EVRcr1kdAiusF_0"
}
```

后端返回更新后的access
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5NzQ4MDgzLCJpYXQiOjE3Mjk3NDcyNzYsImp0aSI6ImU3NWZkNzIwOWIxZTRhZGU5MDk2ZTc1Zjc4MzQwMzI5IiwidXNlcl9pZCI6MX0.wQ9aMBMwgkyGbWKfCK_8cRvBcq2rNvPd_wPNW9kG7BA"
}
```

若refresh错误，后端返回
```json
{
    "code": "token_not_valid",
    "detail": "Token is invalid or expired"
}
```