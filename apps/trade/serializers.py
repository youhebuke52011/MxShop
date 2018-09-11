# -*- coding: utf-8 -*-#
__author__ = 'li'

import time
from rest_framework import serializers

from .models import ShoppingCart, OrderInfo, OrderGoods
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


class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerialzier(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)

    def generate_order_sn(self):
        # 当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id, ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"