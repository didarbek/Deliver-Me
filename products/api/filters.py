from django_filters import FilterSet, AllValuesFilter
from django_filters import DateTimeFilter, NumberFilter, CharFilter

from products.models import Product


class ProductFilter(FilterSet):
    category = AllValuesFilter(field_name='category__title', lookup_expr='iexact')
    delivery = AllValuesFilter(field_name='delivery_type__type', lookup_expr='iexact')
    condition = AllValuesFilter(field_name='condition', lookup_expr='iexact')
    tag = AllValuesFilter(field_name='tags__title', lookup_expr='iexact')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = (
            'category',
            'delivery_type',
            'condition',
            'price',
            'tags'
        )
