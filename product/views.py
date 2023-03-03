from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, \
    ProductCreateSerializer, ProductUpdateSerializer, CategorySerializer, TagSerializer
from .models import Product, Category, Tag
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class TagModelViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        name = serializer.validated_data.get('name')
        text = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        amount = serializer.validated_data.get('quantity')
        is_active = serializer.validated_data.get('is_active')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')
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
        serializer = ProductUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product.name = serializer.validated_data.get('name')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.quantity = serializer.validated_data.get('quantity')
        product.is_active = serializer.validated_data.get('is_active')
        product.category_id = serializer.validated_data.get('category_id')
        product.tags.set(serializer.validated_data.get('tags'))
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
