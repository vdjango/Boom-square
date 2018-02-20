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


from django.contrib.auth.decorators import login_required
import markdown
from app.utli import datetimenow


class log():
    def d(l, arg):
        print('Log.d:', l, arg)
        pass


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
            value.append({"title": i.title, "content": mark, "username": str(i.username),
                          "time_now": str(data).split('.')[0], "id": ids})
            time_date = str(data).split('.')[0]
            log.d('value.append', 'Add')

        else:
            log.d('value_dict', 'Add')
            value_dict[str(Inits)] = {
                'time': time_date,
                'contents_dicts': value
            }
            value = []
            Inits = int(number)

    if len(value) > 1:
        log.d('len(value)', len(value))
        value_dict[str(Inits)] = {
            'time': time_date,
            'contents_dicts': value
        }
        value = []
        Inits = int(number)

    content = {
        'username': str(username),
        'value_dict': value_dict
    }

    log.d('content', content)

    # return HttpResponse(json.dumps(content_list1))

    return render(request, 'home/home.html', content)
