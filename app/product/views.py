"""
Views for the user API.
"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.settings import api_settings

from product import serializers
from core.models import (
    BrandName,
    Category,
)


class BrandView(viewsets.ViewSet):
    """
    API View that returns a BrandName.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    serializer_class = serializers.BrandSerializer

    def list(self, request):
        """
        Return a list of all BrandNames.
        """
        # user = request.user.id
        queryset = BrandName.objects.all()
        serializer = serializers.BrandSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new BrandName.
        """
        serializer = serializers.BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Return a BrandName.
        """
        queryset = BrandName.objects.all()
        brandname = generics.get_object_or_404(queryset, pk=pk)
        serializer = serializers.BrandSerializer(brandname)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
        Partial Update a BrandName.
        """
        queryset = BrandName.objects.get(id=pk)
        if queryset is None:
            return Response(
                {"message": "BrandName not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        queryset.brand_name = request.data.get("brand_name", queryset.brand_name)
        queryset.brand_discription = request.data.get(
            "brand_discription", queryset.brand_discription
        )
        queryset.save()
        serializer = serializers.BrandSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """
        Update a BrandName.
        """
        queryset = BrandName.objects.get(id=pk)
        if queryset is None:
            return Response(
                {"message": "BrandName not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = serializers.BrandSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete a BrandName.
        """
        queryset = BrandName.objects.all()
        if queryset is None:
            return Response(
                {"message": "BrandName not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryView(viewsets.ViewSet):
    """
    API View that returns a Category.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    serializer_class = serializers.CategorySerializer

    def list(self, request):
        """
        Return a list of all Category.
        """
        queryset = Category.objects.all()
        serializer = serializers.CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new Category.
        """
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Return a Category.
        """
        queryset = Category.objects.all()
        category = generics.get_object_or_404(queryset, pk=pk)
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update a Category.
        """
        queryset = Category.objects.all()
        category = generics.get_object_or_404(queryset, pk=pk)
        serializer = serializers.CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Partial Update a BrandName.
        """
        queryset = Category.objects.get(id=pk)
        if queryset is None:
            return Response(
                {"message": "BrandName not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        queryset.category = request.data.get("category", queryset.category)
        queryset.category_discription = request.data.get(
            "category_discription", queryset.category_discription
        )
        queryset.save()
        serializer = serializers.CategorySerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        Delete a Category.
        """
        queryset = Category.objects.all()
        category = generics.get_object_or_404(queryset, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
