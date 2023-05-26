"""
URL mappings for the user API.
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('user/', views.GetUserView.as_view(), name='user'),
    path('user/update', views.UpdateUserView.as_view(), name='user-update'),
    path('user/delete', views.DeleteUserView.as_view(), name='user-delete'),
    path(
        "login/", views.MyTokenObtainPairView.as_view(), name="login"
    ),
    path(
        "login/refresh/", TokenRefreshView.as_view(), name="login_refresh"
    ),
]
# Path: app\user\views.py
