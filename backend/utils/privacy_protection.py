from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import base64, hashlib
from decouple import config


class PrivacyProtection:

    @classmethod
    def decrypt_password(cls, encrypted_password):  # 私钥解密密码

        key_path = config("PRIVATE_KEY_PATH")
        with open(key_path, "r") as key_file:
            private_key = RSA.import_key(key_file.read())

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
