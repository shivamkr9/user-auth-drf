"""
URL mappings for the Product API.
"""
from django.urls import path, include
from product import views
from rest_framework import routers

app_name = "product"
router = routers.DefaultRouter()
router.register("brand", views.BrandView, basename="brand")
router.register("category", views.CategoryView, basename="category")


urlpatterns = [
    path("", include(router.urls)),
]
