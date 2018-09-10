# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd


# 一个相对底层的实现方法
# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Goods.objects.create(**validated_data)


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # fields = ('name', 'click_num', 'market_price', 'add_time')
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandsSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(goods_ins, many=False,
                                         context={"request": self.context["request"]}).data
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) |
                                         Q(category__parent_category_id=obj.id) |
                                         Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True,
                                           context={"request": self.context["request"]})
        # context属性为嵌套的serializer传入request数据，在此主要功能为子serializer传入请求的ip网络地址。
        return goods_serializer.data  # modelmixin源码当中可查看这种样式的编码。返回serializer对象的data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
