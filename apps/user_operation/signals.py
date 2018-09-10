# -*- coding: utf-8 -*-

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_operation.models import UserFav


@receiver(post_save, sender=UserFav)
def create_user_fav(sender, instance=None, created=False, **kwargs):  # 此处函数名不影响
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_user_fav(sender, instance=None, created=False, **kwargs):  # 此处函数名不影响
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
