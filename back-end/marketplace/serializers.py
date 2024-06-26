from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Comment,
    Product,
    ProductImage,
    Category,
    Bookmark,
)

User = get_user_model()


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True, allow_empty_file=False, use_url=False)

    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "description"]

    def validate_product(self, value):
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Product does not exist")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "merchant",
            "category",
            "product_name",
            "price",
            "in_stock",
            "tag",
            "brand",
            "key_features",
            "description",
        ]

    def validate_merchant(self, value):
        if User.objects.get(id=value.id).user_type != "merchant":
            raise serializers.ValidationError("User is not a merchant")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "category_name",
            "sub_category",
        ]


class CommentSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=True, max_length=500)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "product",
            "comment",
            "created_at",
        ]

    def validate_product(self, value):
        product = Product.objects.get(id=value.id)
        if not product:
            raise serializers.ValidationError("Product does not exist")
        return product


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "user", "product_id", "favorite"]
