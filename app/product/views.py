"""
Views for the user API.
"""
from rest_framework import generics, permissions
from user.serializers import (
    UserSerializer,
)
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# from core import models


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to add custom claims."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["name"] = user.name
        token["is_active"] = user.is_active
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    """Custom token view to add custom claims."""

    serializer_class = MyTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class GetUserView(generics.RetrieveAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UpdateUserView(generics.UpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


# class DeleteUserView(generics.DestroyAPIView):
#     """Manage the authenticated user."""

#     serializer_class = UserSerializer
#     authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
#     permission_classes = [
#             permissions.IsAdminUser |
#             custompermission.IsEmployeeUser
#         ]

#     def get_object(self):
#         """Retrieve and return the authenticated user."""
#         return self.request.user
