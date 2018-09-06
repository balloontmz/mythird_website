# -*- coding: utf-8 -*-
import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from mythird_website.settings import REGEX_MOBILE
from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )]

        fields = ("user", "goods", "id")


class LeavingMsgSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")  # add_time格式化=>输入输出？还是只有输出

    class Meta:
        model = UserLeavingMessage
        fields = ("id", "user", "message_type", "subject", "message", "file", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    signer_mobile = serializers.CharField(max_length=11, label="手机号码")

    def validate_signer_mobile(self, signer_mobile):  # 函数的名称必须是validate+字段名
        """
        验证手机号码
        :param data:
        :return:
        """
        # 验证手机号码
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("手机号码非法")

        return signer_mobile

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "signer_mobile")
