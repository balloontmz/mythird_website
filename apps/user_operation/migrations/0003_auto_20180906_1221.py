# Generated by Django 2.0.1 on 2018-09-06 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0002_auto_20180905_1950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userleavingmessage',
            old_name='msg_type',
            new_name='message_type',
        ),
        migrations.AlterField(
            model_name='userfav',
            name='goods',
            field=models.ForeignKey(help_text='商品id', on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品'),
        ),
    ]
