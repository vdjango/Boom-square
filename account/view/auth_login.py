#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-09 01:30:20
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render


def auth_main(request):
    username = request.POST.get('email')
    password = request.POST.get('password')
    auth_acc, auth_err = auth_login_access(request, username, password)
    if auth_acc:
        return auth_return_home()
    else:
        return auth_return_render(request, username, password, auth_err)


def auth_login_access(request, username, password):
    ''' 用户登录认证 '''

    if not username and not password:
        return False, '请输入用户名和密码！'

    if not username:
        return False, '请输入用户名！'

    if not password:
        return False, '请输入密码！'

    if len(username) < 3 and len(password) < 8:
        return False, '用户名和密码应大于3和8位数！'

    if len(username) > 18 and len(password) > 24:
        return False, '用户名和密码应大于3和8位数！'

    if len(username) < 3:
        return False, '用户名应大于3位数！'

    if len(username) > 18:
        return False, '用户名应小于18位数！'

    if len(password) < 8:
        return False, '密码应大于8位数！'

    if len(password) > 24:
        return False, '密码应小于24位数！'

    if not password:
        return False, '请输入密码！'

    user = authenticate(username=username, password=password)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            login(request, user)
            return True, None

        else:
            return False, '密码有效，但帐户已被禁用！'

    else:
        # the authentication system was unable to verify the username and password
        return False, '用户名和密码不正确。'


def auth_logouts(request):  # 用户注销
    logout(request)
    return auth_return_Redirect()


def auth_return_render(request, username=None, password=None, error=None):
    return render(request, 'auth/login.html', {'email': username, 'password': password, 'error': error})


def auth_return_Redirect():
    return HttpResponseRedirect('/auth/login')


def auth_return_home():
    return HttpResponseRedirect('/user/')
