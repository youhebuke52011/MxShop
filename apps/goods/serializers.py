# -*- coding: utf-8 -*-#
__author__ = 'li'

from rest_framework import serializers

from goods.models import Goods, GoodsCategory

# class GoodSerializer(serializers.Serializer):
#     goods_sn = serializers.CharField(max_length=50)
#     name = serializers.CharField(required=True, max_length=100)


class CategorySerializer3(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = "__all__"
        # fields = (
        #     'category',
        #     'goods_sn',
        #     'name',
        #     'click_num',
        #     'goods_desc',
        #     'goods_front_image',
        #     'add_time',
        # )