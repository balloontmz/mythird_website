from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from trade.models import ShoppingCart
from trade.serializers import ShopCartSerializer, ShopCartDetailSerializer
from trade.models import ShoppingCart
from utils.permissions import IsOwnerOrReadOnly


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能开发
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物记录
    read:
        返回指定商品id的购物车记录
    """
    # queryset = ShoppingCart.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 对象级别认证
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)  # 验证是否为登录用户,拥有的用户。
    # serializer_class = ShopCartSerializer  # 动态加载了serializer了，此行应该能够注释掉？
    lookup_field = "goods_id"  # retrieve方法

    def get_queryset(self):  # list方法
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

