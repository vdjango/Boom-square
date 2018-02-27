#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-25 21:25:09
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from app.models import App_Blog


def pers_app(request, tid=None):
    def wrapper(func):
        def sub_wrapper(*args, **kwargs):
            print("定义一个带参数的装饰器", tid)

            tid_con = App_Blog.objects.filter(id=tid)
            tid_user = tid_con.username

            username = request.user.username

            if tid_user != username:
                return

            func(*args, **kwargs)
        return sub_wrapper
    return wrapper
