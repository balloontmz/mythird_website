# Generated by Django 2.0.1 on 2018-09-06 19:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0005_auto_20180903_2214'),
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='goods_num',
            new_name='nums',
        ),
        migrations.AlterUniqueTogether(
            name='shoppingcart',
            unique_together={('user', 'goods')},
        ),
    ]