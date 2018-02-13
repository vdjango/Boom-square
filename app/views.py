#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-05 19:01:27
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.shortcuts import render
from django.http import HttpResponseRedirect
from app import models


# from .models import Blog
# import markdown
# Create your views here.


def admin(request):
    username = request.GET.get("username")
    print(username)
    return render(request, "login.html")


def blogs(request):
    return render(request, "blog.html")


def App_get(request):
    messages = {'messages': models.App_GET_Text_all()}
    return messages


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        username = request.user.username

        if title and content:
            models.App_SAVE_Text(username, title, content)

            return HttpResponseRedirect('/')
        else:
            content = {'title': title,
                       'content': content, 'err': u'不能为空'}

            return render(request, 'create.html', content)
