# -*- coding: utf-8 -*-
__author__ = 'tomtiddler'

# 独立使用django的model
import sys
import os
# 先初始化环境
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+'../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mythird_website.settings')  # 单独使用model必须拿过来 manage中

import django
django.setup()

# 然后使用model
from goods.models import GoodsCategory

from db_tools.data.category_data import row_data

for lev1_ca in row_data:
    lev1_instance = GoodsCategory()
    lev1_instance.code = lev1_ca['code']
    lev1_instance.name = lev1_ca['name']
    lev1_instance.category_type = 1
    lev1_instance.save()

    for lev2_ca in lev1_ca['sub_categorys']:
        lev2_instance = GoodsCategory()
        lev2_instance.code = lev2_ca['code']
        lev2_instance.name = lev2_ca['name']
        lev2_instance.category_type = 2
        lev2_instance.parent_category = lev1_instance  # 二级类有父类
        lev2_instance.save()

        for lev3_ca in lev2_ca['sub_categorys']:
            lev3_instance = GoodsCategory()
            lev3_instance.code = lev3_ca['code']
            lev3_instance.name = lev3_ca['name']
            lev3_instance.category_type = 3
            lev3_instance.parent_category = lev2_instance  # 三级类有父类
            lev3_instance.save()
