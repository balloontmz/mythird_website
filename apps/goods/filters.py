# -*- coding: utf-8 -*-

from django.db.models import Q
from django_filters import rest_framework as filters
from goods.models import Goods


class GoodsFilter(filters.FilterSet):  # drf的Filters对该功能进行了拓展
    """
    商品的过滤类
    """
    pricemin = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    # name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    top_category = filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) |
                               Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', "is_new"]
