"""
Views for the user API.
"""
from rest_framework import generics, permissions
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from api import custompermission  # noqa

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from user import serializers
from core.models import (
    State,
    District,
)

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


class StateView(viewsets.ViewSet):
    """
    Viewset for State.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    serializer_class = serializers.StateSerializer

    def list(self, request):
        """
        Return a list of all State.
        """
        queryset = State.objects.all()
        serializer = serializers.StateSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new State.
        """
        serializer = serializers.StateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Return a State.
        """
        queryset = State.objects.all()
        state = generics.get_object_or_404(queryset, pk=pk)
        serializer = serializers.StateSerializer(state)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update a State.
        """
        state = State.objects.get(pk=pk)
        serializer = serializers.StateSerializer(state, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete a State.
        """
        queryset = State.objects.get(id=pk)
        if queryset is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DistrictView(viewsets.ModelViewSet):
    """District viewset for CRUD operations."""

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    serializer_class = serializers.DistrictSerializer
    queryset = District.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    """Custom token view to add custom claims."""

    serializer_class = MyTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = serializers.UserSerializer


class GetUserView(generics.RetrieveAPIView):
    """Manage the authenticated user."""

    serializer_class = serializers.UserSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UpdateUserView(generics.UpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = serializers.UserSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
