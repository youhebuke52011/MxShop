# -*- coding: utf-8 -*-#
__author__ = 'li'

import re
from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if User.object.filter(mobile=mobile).exists():
            raise serializers.ValidationError("用户已经存在")

        # 手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")

        # 验证码是否过期
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).exists():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile