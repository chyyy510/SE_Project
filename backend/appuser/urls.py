from django.urls import path
from appuser.views import (
    UserList,
    UserDetail,
    UserRegister,
    UserLogin,
    UserTokenRefresh,
    UserProfileDetail,
    UserProfileAvatarUpload,
    UserProfileEdit,
)

urlpatterns = [
    path("", UserList.as_view(), name="user-list"),
    path("detail/", UserDetail.as_view(), name="user-detail"),
    path("register/", UserRegister.as_view(), name="user-register"),
    path("login/", UserLogin.as_view(), name="user-login"),
    path("token/refresh/", UserTokenRefresh.as_view(), name="token-refresh"),
    path("profile/", UserProfileDetail.as_view(), name="user-profile"),
    path(
        "profile/update/avatar/",
        UserProfileAvatarUpload.as_view(),
        name="avatar-upload",
    ),
    path("profile/edit/", UserProfileEdit.as_view(), name="user-profile-edit"),
]
