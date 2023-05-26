"""
Django API URL Configuration.
"""
from django.contrib import admin
from django.urls import path, include  # noqa
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/", SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="docs"
    ),
    path(
        "api/redoc/", SpectacularRedocView.as_view(url_name="api-schema"),
        name="redoc"
    ),
    path("api/", include("user.urls"), name="user"),
]
