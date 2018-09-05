from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav
from user_operation.serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.
class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    用户收藏功能
    """
    queryset = UserFav.objects.all()  # 由于某些第三方包的依赖问题此行需要保留
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 对象级别认证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 验证是否为登录用户,拥有的用户。
    serializer_class = UserFavSerializer

    def get_queryset(self):  # 此过滤条件暂时可以直接写入queryset的过滤。
        return self.queryset.filter(user=self.request.user)
