"""
URL mappings for the user API.
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from user import views


app_name = "user"

urlpatterns = [
    path("", views.GetUserView.as_view(), name="get-user"),
    path("create/", views.CreateUserView.as_view(), name="create-user"),
    path("update", views.UpdateUserView.as_view(), name="update-user"),
    path("login/", views.MyTokenObtainPairView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
]
# Path: app\user\views.py
