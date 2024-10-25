from django.urls import path
from appuser.views import (
    UserList,
    UserDetail,
    UserRegister,
    # UserLogin,
    UserTokenRefresh,
    UserProfileDetail,
    UserProfileAvatarUpload,
)

urlpatterns = [
    path("", UserList.as_view(), name="user-list"),
    path("<int:pk>/", UserDetail.as_view(), name="user-detail"),
    path("register/", UserRegister.as_view(), name="user-register"),
    # path("login/", UserLogin.as_view(), name="user-login"),
    path("token/refresh/", UserTokenRefresh.as_view(), name="token-refresh"),
    path("profile/", UserProfileDetail.as_view(), name="user-profile"),
]
