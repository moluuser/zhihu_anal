# Generated by Django 3.0.8 on 2020-07-12 02:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0003_zhihu_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Zhihu_user',
            new_name='ZhihuUser',
        ),
    ]