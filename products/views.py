from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer, ProductDetailSerializer
from django.db import transaction


@api_view(http_method_names=['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        # step 1: Collect products from DB (QuerySet)
        products = (Product.objects.select_related('category')
                    .prefetch_related('tags', 'reviews').filter(is_active=True))

        # step 2: Reformat QuerySet to list of dictionary (Serializer)
        data = ProductSerializer(products, many=True).data

        # step 3: Return Response
        return Response(data=data)  # data = dict / list / list of dict
    elif request.method == 'POST':
        # step 1: Receive data from RequestBody
        name = request.data.get('name')
        text = request.data.get('text')
        price = request.data.get('price')
        is_active = request.data.get('is_active')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')

        # step 2: Create product by received data
        with transaction.atomic():
            product = Product.objects.create(
                name=name,
                text=text,
                price=price,
                is_active=is_active,
                category_id=category_id,
            )
            product.tags.set(tags)
            product.save()

        # step 3: Return response (data=product, status=201)
        return Response(data=ProductDetailSerializer(product).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        product.name = request.data.get('name')
        product.text = request.data.get('text')
        product.category_id = request.data.get('category_id')
        product.price = request.data.get('price')
        product.is_active = request.data.get('is_active')
        product.tags.set(request.data.get('tags'))
        product.save()
        return Response(data=ProductDetailSerializer(product).data,
                        status=status.HTTP_201_CREATED)
