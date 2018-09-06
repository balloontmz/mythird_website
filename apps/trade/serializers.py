# -*- coding: utf-8 -*-
__author__ = 'tomtiddler'

from rest_framework import serializers

from trade.models import ShoppingCart
from goods.models import Goods


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, label="数量",
                                    error_messages={
                                        "min_value": "商品数量不能小于1",
                                        "required": "请填写购买数量",
                                    })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True, label="商品")

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        # 为什么此处直接是实例，猜测和retrieve方法相关。
        instance.nums = validated_data["nums"]
        instance.save()
        return instance
