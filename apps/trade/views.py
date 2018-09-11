from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permission import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderInfoSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    list:
        购物车列表
    create:
        添加购物车
    destroy:
        删除购物车
    update:
        更新购物车
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    lookup_field = "goods_id"

    # serializer_class = ShopCartSerializer
    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderInfoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderInfoSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderInfoSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        for shop_cart in ShoppingCart.objects.filter(user=self.request.user):
            order_goods = OrderGoods()
            order_goods.order = order
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.save()
            shop_cart.delete()
        return order

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)
