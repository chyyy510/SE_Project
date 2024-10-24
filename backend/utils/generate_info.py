from appuser.models import User
from django.db.models import Max


class GenerateInfo:

    @classmethod
    def generate_uid(cls):
        max_uid = User.objects.aggregate(Max("uid"))["uid__max"]
        if max_uid == None:
            max_uid = 1000000
        max_uid += 1
        return max_uid
