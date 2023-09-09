from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = UsersConfig.name

# Урлы для приложения пользователя с токенами
urlpatterns = [
    path("create/", UserCreateAPIView.as_view(), name="user_create"),
    path("list/", UserListAPIView.as_view(), name="user_list"),
    path(
        "deteil/<int:pk>/",
        UserRetrieveAPIView.as_view(),
        name="user_deteil",
    ),
    path(
        "update/<int:pk>/",
        UserUpdateAPIView.as_view(),
        name="user_update",
    ),
    path(
        "delete/<int:pk>/",
        UserDestroyAPIView.as_view(),
        name="user_delete",
    ),
    # Работа с токенами
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]