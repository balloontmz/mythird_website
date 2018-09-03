# -*- coding: utf-8 -*-

from django_filters import rest_framework as filters
from goods.models import Goods


class GoodsFilter(filters.FilterSet):
    """
    商品的过滤类
    """
    min_price = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    # name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ['min_price', 'max_price']
