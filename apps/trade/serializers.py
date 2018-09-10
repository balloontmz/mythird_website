# -*- coding: utf-8 -*-
__author__ = 'tomtiddler'

import time
from random import Random

from rest_framework import serializers

from trade.models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSerializer
from utils.alipay import Alipay
from mythird_website.settings import ali_pub_key_path, private_key_path


class ShopCartDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


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

        goods.goods_num -= nums
        goods.save()

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        # 为什么此处直接是实例，猜测和retrieve方法相关。
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = Alipay(
            appid="2016091600527206",
            app_notify_url="https://120.79.157.29:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            debug=True,
            return_url="https://120.79.157.29:8001/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    # 个人猜测此属性只是隐藏，并设置默认值，并不能防止权限，权限由其他设置搞定
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = Alipay(
            appid="2016091600527206",
            app_notify_url="https://120.79.157.29:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            debug=True,
            return_url="https://120.79.157.29:8001/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    def generate_order_sn(self):
        # 当前时间+user_id+随机数
        random_ins = Random()
        order_sn = "{time_str}{user_id}{ran_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                         user_id=self.context["request"].user.id,
                                                         ran_str=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
