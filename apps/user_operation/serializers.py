# -*- coding: utf-8 -*-#
__author__ = 'li'

import re
from rest_framework import serializers

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodSerializer
from MxShop.settings import REGEX_MOBILE


class UserfavDetailSerializer(serializers.ModelSerializer):
    goods = GoodSerializer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        fields = ('user', 'goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    def validate_signer_mobile(self, signer_mobile):
        """
        验证手机号码
        :return:
        """
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("手机号码不合法")
        return signer_mobile

    class Meta:
        model = UserAddress
        fields = "__all__"
