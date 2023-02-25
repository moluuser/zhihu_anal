from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=255, default='管理员')

    class Meta:
        db_table = 'user'


class ZhihuUser(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    company = models.CharField(max_length=255)

    class Meta:
        db_table = 'zhihu_user'


class ZhihuQue(models.Model):
    title = models.CharField(max_length=255)
    follow = models.CharField(max_length=255)
    pageview = models.CharField(max_length=255)

    class Meta:
        db_table = 'zhihu_que'


class ZhihuTag(models.Model):
    name = models.CharField(max_length=255)
    count = models.CharField(max_length=255)

    class Meta:
        db_table = 'zhihu_tag'
