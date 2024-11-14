# user/views.py
from rest_framework import viewsets

from user.models import Users
from user.serializer import UsersSerializer


class userViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer