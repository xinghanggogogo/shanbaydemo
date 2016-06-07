# -*- coding:utf-8 -*-
def permission_check(user): #单纯的定义了一个函数

    if user.is_authenticated():
        return user.myuser.permission > 1
    else:
        return False