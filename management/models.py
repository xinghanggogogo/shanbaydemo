# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User #导入系统自带的用户数据库

# Create your models here.


class MyUser(models.Model):                  #定义了myuser权限等于1
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username    #注意base.html中判断用户权限的语句书写 user.myuser.permission > 1


class Book(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    author = models.CharField(max_length=128)
    publish_date = models.DateField()
    category = models.CharField(max_length=128)

    class META:
        ordering = ['name']  #排倒叙：ordeing = (-'name')

    def __unicode__(self):
        return self.name


class Img(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    img = models.ImageField(upload_to='image/%Y/%m/%d/')  #上传位置！
    book = models.ForeignKey(Book)  #外键  （注意在后台中的对应形式）

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name