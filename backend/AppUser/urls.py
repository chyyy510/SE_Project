from django.urls import path
from appuser.views import UserList, UserDetail

urlpatterns = [
    path("", UserList.as_view(), name="user-list"),
    path("<int:pk>/", UserDetail.as_view(), name="user-detail"),
]
