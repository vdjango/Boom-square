#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-05 19:01:27
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.shortcuts import render
from django.http import HttpResponseRedirect
from app import models
from account.permiss.auth_permissions import user_admin

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


from django.contrib.auth.decorators import login_required
import markdown
from app.utli import datetimenow


class log():
    def d(l, arg):
        print('Log.d:', l, arg)


@login_required(login_url='/auth/login/')
def user_home(request):
    cont = models.App_GET_Text_all()

    # content_dict = {}
    value_dict = {}
    # conlist_dict = {}
    value = []
    # contents_dicts = {}

    time_date = '2018-01-01 00:00:00'

    username = request.user.username

    Inits = 0

    for i in cont:
        ids = i.id
        data = datetimenow.datetimenow(i.time_now)
        mark = markdown.markdown(i.content)
        __, number = datetimenow.DateTimes(str(data).split('.')[0])

        if int(Inits) == int(number):
            value.append({
                "title": i.title,
                "content": mark,
                "username": str(i.username),
                "time_now": str(data).split('.')[0],
                "id": ids}
            )

            time_date = str(data).split('.')[0]
            log.d('value.append', 'Add')

        else:
            if time_date != '2018-01-01 00:00:00' and value:
                log.d('value_dict', 'Add')
                value_dict[str(Inits)] = {
                    'time': time_date,
                    'contents_dicts': value
                }

            value = []
            Inits = int(number)

        log.d('len(value)', str(len(value)) + ' ,' + str(number))

    if len(value) > 1:
        if time_date != '2018-01-01 00:00:00' and value:
            log.d('len(value)', len(value))
            value_dict[str(Inits)] = {
                'time': time_date,
                'contents_dicts': value
            }

        value = []
        Inits = int(number)

    content = {
        'username': str(username),  # 用户名称
        'admin': user_admin(str(username)),  # 超级管理员
        'value_dict': value_dict  # 文章等等
    }

    log.d('content', content)

    return render(request, 'home/home.html', content)


@login_required(login_url='/auth/login/')
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        username = request.user.username

        if title and content:
            models.App_SAVE_Text(username, title, content)

            return HttpResponseRedirect('/')
        else:
            content = {
                'title': title,
                'content': content,
                'err': u'不能为空'
            }

            return render(request, 'create.html', content)
