import random
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from django_filters import rest_framework as rest_filters

from products.models import Product, ProductCategory
from products.api.permissions import IsProductSellerOrReadOnly
from products.api.views.browsing_history import add_history_element
from products.api.filters import ProductFilter
from products.api.serializers.product_serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    ProductCategoryTreeSerializer
)


class ProductsListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['title', 'description']


class CurrentUserProductsListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['title', 'description']

    def get_queryset(self):
        products = Product.objects.filter(seller=self.request.user)
        return products


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        product = get_object_or_404(Product, id=self.kwargs['id'])
        user_id = self.request.user
        if user_id:
            add_history_element(user_id=self.request.user, product_id=product.id)
        return product


class UserProductsListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filters_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        products = Product.objects.filter(seller__username=self.kwargs['username'])
        return products


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Product.objects.filter(id=self.kwargs['id'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.seller == request.user or request.user.is_superuser:
            self.perform_destroy(instance)
            return Response({'Your product has been successfully deleted.'}, status=status.HTTP_200_OK)

        return Response({'You are not allowed to do this action.'}, status=status.HTTP_403_FORBIDDEN)


class ProductCategoriesListAPIView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryTreeSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([AllowAny])
def get_recommendations(request):
    product_category = request.GET.get('product_category')
    recommended_products = list(Product.objects.filter(category__title=product_category))
    if recommended_products and len(recommended_products) >= 5:
        random_products = random.sample(recommended_products, 5)
        serializer = ProductSerializer(random_products, many=True)
        return Response({
            'message': 'Here is your recommended products.',
            'data': serializer.data
        })

    return Response({
        'message': 'There are no products that is suitable for you right now.',
        'data': None
    })
