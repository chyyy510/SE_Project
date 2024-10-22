# 放置一些工具函数


class GenerateInfo:
    uid_now_max = 1000000

    @classmethod
    def generate_uid(cls):
        cls.uid_now_max += 1
        return cls.uid_now_max
