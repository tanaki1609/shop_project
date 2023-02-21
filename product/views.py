from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product, Category


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        """ List of objects """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        """ Creation of object """
        name = request.data.get('name')
        text = request.data.get('description')
        price = request.data.get('price')
        amount = request.data.get('quantity')
        is_active = request.data.get('is_active')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')
        product = Product.objects.create(name=name, description=text, price=price,
                                         quantity=amount, is_active=is_active,
                                         category_id=category_id)
        product.tags.set(tags)
        product.save()
        return Response(data={'message': 'Data received!',
                              'product': ProductSerializer(product).data},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'detail': 'product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=False)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        product.name = request.data.get('name')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.quantity = request.data.get('quantity')
        product.is_active = request.data.get('is_active')
        product.category_id = request.data.get('category_id')
        product.tags.set(request.data.get('tags'))
        product.save()
        return Response(data={'message': 'Data received!',
                              'product': ProductSerializer(product).data})


@api_view(['GET', 'POST'])
def test_api(request):
    dict_ = {
        'text': "Hello world",
        'int': 100,
        'float': 9.99,
        'bool': True,
        'list': [1, 2, 3]
    }
    return Response(data=dict_, status=status.HTTP_204_NO_CONTENT)
