# -*- coding: utf-8 -*-
import re
from datetime import datetime
from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import VerifyCode
from mythird_website.settings import REGEX_MOBILE

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):  # 函数的名称必须是validate+字段名
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile=mobile):
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证上一次发送时间
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)  # timedelta函数
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile
