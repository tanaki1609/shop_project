from rest_framework import serializers
from .models import Product, Category, Tag, Review


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
    filtered_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = 'id name tags category category_name tag_name_list ' \
                 'filtered_reviews'.split()
        # exclude = ['price', 'name']

    def get_tag_name_list(self, obj):
        l = []
        for tag in obj.tags.all():
            l.append(tag.name)
        return l
