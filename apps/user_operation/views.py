from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from utils.permission import IsOwnerOrReadOnly
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserfavDetailSerializer, LeavingMessageSerializer, UserAddressSerializer


class UserFavViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    destroy:
    取消收藏

    list:
    收藏列表

    create:
    添加收藏
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    # serializer_class = UserFavSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return UserfavDetailSerializer
        else:
            return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class LeavingMessageViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """
    create:
        添加留言
    destroy:
        删除留言
    list:
        留言列表
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    """
    收货地址管理
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
