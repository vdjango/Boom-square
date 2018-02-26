#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-10 10:07:48
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

# from account.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponseRedirect


def auth_main(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    passd = request.POST.get('pass')
    auth_acc, auth_err = auth_register_access(
        request, email, username, password, passd)
    if auth_acc:
        return auth_return_home()
    else:
        return auth_return_render(request, email, username, password, '', auth_err)


def auth_register_access(request, email, username, password, passd):
    ''' 用户登录认证 '''
    if not email and not username and not password:
        return False, '您还没有填写信息哦！'

    elif not email and not username:
        return False, '请输入邮箱和用户名！'

    elif not email and not password:
        return False, '请输入邮箱和密码！'

    elif not username and not password:
        return False, '请输入用户名和密码！'

    elif not username:
        return False, '请输入用户名！'

    elif not password:
        return False, '请输入密码！'

    if not passd:
        return False, '重复密码不能为空！'

    if password != passd:
        return False, '重复密码不一致！'

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

    u = authenticate(email=email, username=username, password=password)
    if u:
        return False, '用户已注册'

    # the password verified for the user
    from django.contrib.auth.models import User
    from account.permiss import auth_permissions
    user = User.objects.create_user(username, email, password)
    user.save()
    auth_permissions.add_group_default(username)

    login(request, authenticate(email=email, username=username, password=password))
    return auth_return_login(request), '注册成功！'


def auth_return_login(request):
    return HttpResponseRedirect('/auth/login/')


def auth_return_render(request, email=None, username=None, password=None, passd=None, error=None):
    return render(request, 'auth/register.html', {'email': email, 'username': username, 'password': password, 'email': email, 'error': error})


def auth_return_Redirect():
    return HttpResponseRedirect('/auth/register/')


def auth_return_home():
    return HttpResponseRedirect('/user/')
