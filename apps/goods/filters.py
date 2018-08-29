# -*- coding: utf-8 -*-#
__author__ = 'li'

from django.db.models import Q
import django_filters
from .models import Goods


class GoodFilter(django_filters.rest_framework.FilterSet):

    price_min = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    name = django_filters.CharFilter(field_name='name',lookup_expr='contains')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(
            Q(category_id=value) |
            Q(category__parent_category_id=value) |
            Q(category__parent_category__parent_category_id=value)
        )

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name']