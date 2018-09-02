# -*- coding: utf-8 -*-
__author__ = 'tomtiddler'

import json

from django.views.generic.base import View
# from django.views.generic import ListView

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        :param request:
        :return:
        """
        json_list = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name  # 此处如果直接返回类则无法序列化
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)

        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        from django.core import serializers
        json_data = serializers.serialize('json', goods)
        # json_data = json.loads(json_data)  # 将数据变成dict

        from django.http import HttpResponse
        return HttpResponse(json_data, content_type='application/json')  # json.dumps ->变成json文件
