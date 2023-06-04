from rest_framework import serializers

from core.models import (
    Category,
    BrandName,
)


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for the brand object"""

    class Meta:
        model = BrandName
        fields = ("id", "brand_name", "brand_discription")
        read_only_fields = ("id",)

    def validate(self, attrs):
        brand_name = attrs.get("brand_name")
        bradn_discription = attrs.get("brand_discription")
        if not brand_name or not bradn_discription:
            raise serializers.ValidationError(
                "Pleasea provide brand name and brand discription correctly"
            )
        return super().validate(attrs)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the category object"""

    class Meta:
        model = Category
        fields = ("id", "category", "category_discription")
        read_only_fields = ("id",)

    def validate(self, attrs):
        category_name = attrs.get("category")
        category_discription = attrs.get("category_discription")
        if not category_name or not category_discription:
            raise serializers.ValidationError(
                "Pleasea provide category name and category discription correctly"
            )
        return super().validate(attrs)
