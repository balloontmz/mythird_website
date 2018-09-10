import time
from datetime import datetime
from random import Random

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response

from trade.serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from utils.permissions import IsOwnerOrReadOnly
from utils.alipay import Alipay
from mythird_website.settings import ali_pub_key_path, private_key_path


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

    # 此方法存在漏洞，由于添加购物车有可能是create中的更新操作，此方法无法辨别，而是减去了过多的商品数量
    # def perform_create(self, serializer):
    #     shop_cart = serializer.save()
    #     goods = shop_cart.goods
    #     goods.goods_num -= shop_cart.nums
    #     goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.filter(id=serializer.instance.id)[0]
        existed_nums = existed_record.nums
        save_record = serializer.save()
        nums = save_record.nums - existed_nums
        goods = save_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_queryset(self):  # list方法
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer  # 对应读取功能，购物车不存在读取每一项细节，所以list够了。
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
    # serializer_class = OrderSerializer

    def get_queryset(self):  # list方法
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        else:
            return OrderSerializer

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


class AliPayView(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)
        alipay = Alipay(
            appid="2016091600527206",
            app_notify_url="https://120.79.157.29:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            debug=True,
            return_url="https://120.79.157.29:8001/alipay/return/"
        )

        verify_result = alipay.verify(processed_dict, sign)  # 此处理想返回True

        if verify_result is True:
            order_sn = processed_dict.get("out_trade_no", None)
            trade_no = processed_dict.get("trade_no", None)
            trade_status = processed_dict.get("trade_status", None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")

    def post(self, request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)
        alipay = Alipay(
            appid="2016091600527206",
            app_notify_url="https://120.79.157.29:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            debug=True,
            return_url="https://120.79.157.29:8001/alipay/return/"
        )

        verify_result = alipay.verify(processed_dict, sign)  # 此处理想返回True

        if verify_result is True:
            order_sn = processed_dict.get("out_trade_no", None)
            trade_no = processed_dict.get("trade_no", None)
            trade_status = processed_dict.get("trade_status", None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 交易成功销量增加
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")
