# Generated by Django 2.0.1 on 2018-09-06 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0003_auto_20180906_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='city',
            field=models.CharField(default='', max_length=100, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='province',
            field=models.CharField(default='', max_length=100, verbose_name='省份'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='district',
            field=models.CharField(default='', max_length=100, verbose_name='区域'),
        ),
        migrations.AlterField(
            model_name='userleavingmessage',
            name='file',
            field=models.FileField(help_text='上传的文件', upload_to='message/images/', verbose_name='上传的文件'),
        ),
    ]
