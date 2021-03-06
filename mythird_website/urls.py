"""mythird_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from mythird_website.settings import MEDIA_ROOT

from goods.views import GoodsListViewset, CategoryViewset, BannerViewset, IndexCategoryViewset, HotSearchViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMsgViewset, AddressViewset
from trade.views import ShoppingCartViewset, OrderViewset, AliPayView
# from goods.views_base import GoodsListView
#from goods.views import GoodsListView

# goods_list = GoodsListViewset.as_view({
#     'get': 'list',
# })

router = DefaultRouter()

# viewset重写了as_view才能调用router。其他好像不能？
# 配置商品列表页的url
router.register('goods', GoodsListViewset)

# 配置商品类型的url
router.register('categorys', CategoryViewset)

# 用户注册验证码的url
router.register('code', SmsCodeViewset)

# 用户注册的url
router.register('users', UserViewset, base_name="users")

# 用户收藏的url
router.register('userfavs', UserFavViewset, base_name="userfavs")

# 留言
router.register('messages', LeavingMsgViewset, base_name="messages")

# 收货地址
router.register('address', AddressViewset, base_name="address")

# 购物车功能
router.register('shopcarts', ShoppingCartViewset, base_name="shopcarts")

# 订单功能
router.register('orders', OrderViewset, base_name="orders")

# 轮播图url
router.register('banners', BannerViewset, base_name="banners")

# 首页商品细类数据
router.register('indexgoods', IndexCategoryViewset, base_name="indexgoods")

# 热搜
router.register('hotsearchs', HotSearchViewset, base_name="hotsearchs")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    # 用于api详情页面登录功能
    path('api-auth/', include('rest_framework.urls')),

    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),  # nginx代理了media

    # 商品列表页
    # path('goods/', goods_list, name='goods-list'),

    path('', include(router.urls)),  # 此处为空字符串，切记

    path('docs/', include_docs_urls(title='tomtiddler')),

    # drf自带的认证模式
    path('api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口,登录接口,此处用正则表达式限定内容，防止login之后带参数而导致无法登录第三方
    re_path(r'^login/$', obtain_jwt_token),

    # 支付宝接口，为什么不写入router？还是不能？忘了,应该是apiview没有实现router方法
    path('alipay/return/', AliPayView.as_view()),

    # 第三方登录url, 可查看源码
    path('', include('social_django.urls', namespace='social')),

    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),

]
