# Generated by Django 2.0.1 on 2018-09-05 19:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0005_auto_20180903_2214'),
        ('user_operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together={('user', 'goods')},
        ),
    ]
