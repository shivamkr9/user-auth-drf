"""
URL mappings for the Product API.
"""
from django.urls import path
from product import views


app_name = "product"

urlpatterns = [
    path("", views.GetUserView.as_view(), name="get-product"),
    path("create/", views.CreateUserView.as_view(), name="create-product"),
    path("update", views.UpdateUserView.as_view(), name="update-product"),
]
# Path: app\user\views.py
