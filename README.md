# SE_Project

## 数据传输标准

### User

- user-list:
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

- user-detail:
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

- user-register TODO:暂定只需传递以下字段
```json
{
    "email": "Alice@gmail.com",
    "nickname": "Alice",
    "password_hashed": "wevn852",
}
```
- user-login TODO:暂定只需传递以下字段
```json
{
    "email": "Alice@gmail.com",
    "password_hashed": "wevn852",
}

```