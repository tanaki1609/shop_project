import re

from rest_framework import serializers
from .models import Product, Category, Tag, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id name'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    tag_name_list = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id name description price quantity is_active tags category category_name tag_name_list '.split()
        # exclude = ['price', 'name']

    def get_tag_name_list(self, obj):
        l = []
        for tag in obj.tags.all():
            l.append(tag.name)
        return l


class ProductValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, min_length=2)
    price = serializers.FloatField(max_value=1000000, min_value=0)
    description = serializers.CharField(required=False)
    quantity = serializers.IntegerField(min_value=1)
    is_active = serializers.BooleanField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField())

    def validate_category_id(self, category_id):  # 100
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('This category does not exists!')
        return category_id

    def validate_tags(self, tags):  # [1,2,100]
        tags_db = Tag.objects.filter(id__in=tags)
        if len(tags_db) != len(tags):
            raise ValidationError('Tag does not exists')
        return tags


class ProductCreateSerializer(ProductValidateSerializer):
    pass


class ProductUpdateSerializer(ProductValidateSerializer):
    pass