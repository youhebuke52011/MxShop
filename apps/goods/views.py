from django.shortcuts import render

# Create your views here.

from goods.models import Goods, GoodsCategory
from goods.serializers import GoodSerializer, CategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import mixins

# class SnippetList(APIView):
#     """
#     商品列表
#     """
#     def get(self, request, format=None):
#         rows = Goods.objects.all()[:10]
#         good_serializer = GoodSerializer(rows, many=True)
#         return Response(good_serializer.data)

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


class GoodPagination(PageNumberPagination):
    page_size = 24
    page_query_param = 'p'
    page_size_query_param = 'n'
    max_page_size = 100


# class GoodListView(generics.ListAPIView):
#     # generics.ListAPIView == mixins.ListModelMixin,GenericAPIView
#     queryset = Goods.objects.all()
#     serializer_class = GoodSerializer
#     pagination_class = GoodPagination

from rest_framework import viewsets,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication

from .filters import GoodFilter


class GoodListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodSerializer
    pagination_class = GoodPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = GoodFilter
    search_fields = ('name', 'goods_sn')
    ordering_fields = ('sold_num', 'shop_price')
    # authentication_classes = (TokenAuthentication,)


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer