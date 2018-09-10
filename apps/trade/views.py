from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from utils.permission import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer, ShopCartDetailSerializer
from .models import ShoppingCart


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
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)
