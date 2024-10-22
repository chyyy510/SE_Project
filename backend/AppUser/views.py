from django.shortcuts import render
from appuser.models import User
from appuser.serializers import UserSerializer, UserRegeisterSerializer

from rest_framework import generics

# Create your views here.


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegeisterSerializer
