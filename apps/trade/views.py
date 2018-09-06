import time
from random import Random

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from trade.serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods
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


class OrderViewset(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):  # 订单不允许修改，所以不继承modelviewset
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create:
        新增订单
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 对象级别认证
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)  # 验证是否为登录用户,拥有的用户。
    serializer_class = OrderSerializer

    def get_queryset(self):  # list方法
        return OrderInfo.objects.filter(user=self.request.user)

    # 此功能放到serializer中
    # def generate_order_sn(self):
    #     # 当前时间+user_id+随机数
    #     random_ins = Random()
    #     order_sn = "{time_str}{user_id}{ran_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
    #                                                      user_id=self.request.user.id,
    #                                                      ran_str=random_ins.randint(10, 99))
    #     return order_sn

    def perform_create(self, serializer):  # 生成订单，增加订单商品，清空购物车，
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order
