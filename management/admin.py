# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from management.models import *
#在后台注册你的model
# Register your models here.

class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)

#后台注册
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(Img)
