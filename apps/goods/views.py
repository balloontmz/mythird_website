# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework import generics
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from goods.models import Goods, GoodsCategory, Banner, HotSearchWords
from goods.serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer, HotWordsSerializer
from goods.filters import GoodsFilter


# class GoodsListView(APIView):
#     """
#     List all goods, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         goods_json = GoodsSerializer(goods, many=True)
#         return Response(goods_json.data)
#
#     def post(self, request, format=None):
#         serializer = GoodsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):  # 查看代码
#     """
#     商品列表页
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

# class GoodsListView(generics.ListAPIView):
#     """
#     商品列表页
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = StandardResultsSetPagination  # 此参数及功能在GenericApiView中


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


# class OwnerFilter(filters.OrderingFilter):
#     ordering_param = "fcu"


class GoodsListViewset(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品列表页，分页，搜索，过滤，排序
    read:
        商品详情页
    """
    # throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination  # 此参数及功能在GenericApiView中
    # authentication_classes = (TokenAuthentication, )  # 类内配置用户
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # OwnerFilter
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        类目列表数据
    retrieve:
        获取商品分类的详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分页数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True)
    serializer_class = IndexCategorySerializer


class HotSearchViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜
    """
    queryset = HotSearchWords.objects.all().order_by("-index")[:3]
    serializer_class = HotWordsSerializer