from appuser.models import User, UserOrder
from django.db.models import Max


class GenerateInfo:

    @classmethod
    def generate_uid(cls):
        max_uid = User.objects.aggregate(Max("uid"))["uid__max"]
        if max_uid is None:
            max_uid = 1000000
        max_uid += 1
        return max_uid

    @classmethod
    def generate_trade_no(cls, user_id):
        user = User.objects.get(id=user_id)
        try:
            order = UserOrder.objects.get(user=user)
        except:
            order = UserOrder(user=user, status="ongoing", count=1)
            order.save()

            return order.count

        order.count += 1
        order.save()
        return order.count
