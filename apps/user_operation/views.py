from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMsgSerializer, AddressSerializer
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.
class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        个人中心用户收藏功能
    read:
        是否收藏
    create:
        点击收藏收藏
    delete:
        取消收藏
    """
    # queryset = UserFav.objects.all()  # 由于某些第三方包的依赖问题此行需要保留
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 对象级别认证
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)  # 验证是否为登录用户,拥有的用户。
    # serializer_class = UserFavSerializer
    lookup_field = "goods_id"  # 单项查找时的搜索字段，默认为pk，可能表示model_id。查询是在query_set之后，已经经过了过滤。

    def get_queryset(self):  # 此过滤条件暂时可以直接写入queryset的过滤。
        return UserFav.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer


class LeavingMsgViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    """
    serializer_class = LeavingMsgSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 对象级别认证
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)  # 验证是否为登录用户,拥有的用户。

    def get_queryset(self):  # 此过滤条件暂时可以直接写入queryset的过滤。
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    serializer_class = AddressSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 对象级别认证
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)  # 验证是否为登录用户,拥有的用户。

    def get_queryset(self):  # 此过滤条件暂时可以直接写入queryset的过滤。
        return UserAddress.objects.filter(user=self.request.user)
