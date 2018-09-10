# -*- coding: utf-8 -*-#
__author__ = 'li'

from rest_framework import serializers

from .models import ShoppingCart
from goods.models import Goods
from goods.serializers import GoodSerializer


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("goods", "nums")


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={
                                        "required": "请选择商品数量",
                                        "min_value": "数量不能少于1"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True,
                                               queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        shop_cart = ShoppingCart.objects.filter(user=user, goods=goods)
        if shop_cart.exists():
            shop_cart = shop_cart[0]
            shop_cart.nums += nums
            shop_cart.save()
        else:
            shop_cart = ShoppingCart.objects.create(**validated_data)
        return shop_cart

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance