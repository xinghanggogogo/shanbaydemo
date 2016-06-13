# -*- coding:utf-8 -*-
def permission_check(user): #定义了一个函数，用来判断用户的权限，用户注册是时permission为1.

    if user.is_authenticated():
        return user.myuser.permission > 1
    else:
        return False