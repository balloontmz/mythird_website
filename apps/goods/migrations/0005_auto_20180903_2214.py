# Generated by Django 2.0.1 on 2018-09-03 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20180902_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodscategory',
            name='is_tab',
            field=models.BooleanField(default=False, verbose_name='是否导航'),
        ),
    ]
