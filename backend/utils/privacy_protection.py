from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import base64, hashlib


class PrivacyProtection:

    @classmethod
    def decrypt_password(cls, encrypted_password):  # 私钥解密密码

        private_key = RSA.import_key(
            """-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEAmIzophqDebSpnL77RK0l6l8TECsiW7t1+7ilLuc0OtPBFgRa
    IyEUhjV90XY1LJcWZ3UmdZ77GBoHRcZa0UAE8DF7seDu2yyXy2xE0i4gFo41WhOw
    IkV0SVlT7hQ+llf2w8Nk48efjjpz9v5Nf62IVxRBcDQq3BUbvq/ZHbkUs7jiAIp2
    DeW4FBL3gj7C4yaCkis0HOHFSqCGxDfDr8VgY9quJIoKfLDqMeXylBICW9tAdUSB
    C6nf8fdiFflvdenVb1VhZ64oseJMp+8Bqt5RwTHjucdOXlXbhM+pooTEKu+FyVQc
    wbwkjL0MM8SnZcfozP9ZAlSiO+5vewrqiOhBNwIDAQABAoIBACyiNcO7yDII2QOC
    oXPzkT9kt+goJrJeQ+P1n2b8wLxhjoIJnfHfUOj/p6NsiZxVTHnSvgD2FhN0MiKJ
    KbNFnuxEHiPqYxh/kJ41PGGem0beLt//GK6+UYrQdw0WoUVN0WZvugonMxjjI2Dm
    APjVZinMRGU27j9ccbS2MLlQmK0IfHq21COd1DbfDExbl1wWLIGknOCj2zfH7q5a
    N1V1BPhmn7xHCC57bWywyFH763DSE8+Yr31N3WUnooiuxeIehPmEkArtfPRETKgp
    hyWPD9vp25UOSjCvTdnwQ6hQ7cLIByFUJGPbrWtxGniVbxo5t5ZcNzkh1/jtnssR
    8Nnt5BkCgYEAxDJLbPPeq453bTWCxLYYg66sScFsQN8I1rzqzipIJS20l2pqnj9z
    HsZ0rz1uMX86H9WGxmdgGI5Mm/xWSGn3l7rYvuVW/9K1Kf6EdEIA+BSesYeXbqaw
    kAka9TKOt1WUrFzs27YmZndLd9dG+KfgDbd0DsTeU02cd17KQvLbrwsCgYEAxwzN
    t3TCakZO7nplMLZ3axlB7CST6zLuGcMsXF3K9BYt4j8nA2OhQjnlKRSoTzQAwAyc
    DrKwWz+NkQ2ymufXLYlscj1gfk5pPcjGS1zK9fU7vgTuBl43Sog2xd2aTY/Cqmkr
    ODvYzKlBfc2Bi43Kx8qVG7wiArAjU1ObsbiXQgUCgYEAq0DPb5HK2mqnug7MT1I3
    QbIVNuf7ywAjofUS69QiVzl2+ffsiqcNoF5P+aqgZdoM7T6fvsz7J1QGcN2ontrI
    QIvap35eGz1b3wUHrsbyO5kcEBAv0Wj0kzUvb7mqs0KjXHRcV0e+axBUMo4Zp/A4
    9SAd0Mps2b/UBKob2KZNtZMCgYAKu8gEEonBTVVIStVWESDTZ6NEZpyLXE22me20
    dWJSUzfaMWmbJy408gZHdtO0oatAr+1iZYRZB05M+h4deE8EJ5rvdhvT88p9CGyY
    98ICDV1RW9ayBTaaEEpT1SVS9WOb6NvpxmBkeOQNMp2/tr+ukmAEBNsYpgLhpWqJ
    5NhTOQKBgFvdsoNWjrKNn1gRbH0pusdr9SMNIxJI1OGAPlceaQfs9Dsw1/pYpTM9
    Hg/gRRcuGh+acap13Qm6WHcaeMzSbjPumUFMb1ex5DMM6265oJNX7tcV218E2uoi
    9d8+gXkpxNrsfNLC74EhpS1DvqfYU360tVuGbAzN7Qpszxqw87Om
    -----END RSA PRIVATE KEY-----"""
        )

        # 解码 Base64 字符串
        encrypted_password_bytes = base64.b64decode(encrypted_password)

        # 创建解密器
        cipher = PKCS1_OAEP.new(private_key)

        # 解密
        decrypted_password = cipher.decrypt(encrypted_password_bytes)

        return decrypted_password.decode("utf-8")

    @classmethod
    def hash_password(cls, password, salt):  # 给解密后的密码+salt hash存数据库
        password = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
        return password.hex()
