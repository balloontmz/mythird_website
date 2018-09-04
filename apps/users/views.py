from random import choice

from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from users.serializers import SmsSerializer, UserRegisterSerializer
from utils.yunpian import YunPian
from mythird_website.settings import YUNPIAN_API_KEY
from users.models import VerifyCode

User = get_user_model()


class CustomBackend(ModelBackend):  # 继承自默认配置的类，在setting中配置完之后全局所有应用都适用
    """
    自定义用户验证类
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer
    queryset = VerifyCode.objects.all()  # 此参数必须

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 如果调用失败，抛异常(设置)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(YUNPIAN_API_KEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"],
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)  # 短信发送成功才保存验证码
            code_record.save()
            return Response({
                "mobile": mobile,
            }, status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
