from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer


@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    # step 1: Collect products from DB (QuerySet)
    products = (Product.objects.select_related('category')
                .prefetch_related('tags', 'reviews').filter(is_active=True))

    # step 2: Reformat QuerySet to list of dictionary (Serializer)
    data = ProductSerializer(products, many=True).data

    # step 3: Return Response
    return Response(data=data)  # data = dict / list / list of dict


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)
