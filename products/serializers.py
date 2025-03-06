from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ['id', 'name', 'price', 'created']
        fields = 'id name price created'.split()
        # fields = '__all__'
        # exclude = 'created updated'.split()


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
