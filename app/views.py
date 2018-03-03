#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-05 19:01:27
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.shortcuts import render
from django.http import HttpResponseRedirect
from app import models
from django.contrib.auth.decorators import login_required, permission_required
from app.view import app_index
from account.permiss.auth_permissions import user_admin
from app.utli.xss import xss
from Boom_square.settings import BASE_DIR
ROOT = BASE_DIR


def user_home(request):
    if request.method == 'GET':
        content = app_index.index(request)
        print('content', content)
        return render(request, 'home/home.html', content)


@login_required(login_url='/auth/login/')
@permission_required(perm='app.app_create_article', login_url='/app/info/')
def create(request):
    if request.method == 'GET':
        auth_logins = False
        username = None
        pers = None

        if request.user.is_authenticated():
            username = request.user.username
            pers = user_admin(str(username))
            auth_logins = True

        from app.utli.datetimenow import datetime_unix
        a_tid_unix = "%s" % str(datetime_unix())

        content = {
            'auth_login': auth_logins,
            'username': str(username),  # 用户名称
            'admin': pers,  # 超级管理员
            'unix': a_tid_unix,
        }

        return render(request, 'home/editors.html', content)

    if request.method == 'POST':
        comment_title = request.POST.get('title', '')
        comment_content = request.POST.get('content', '')
        comment_unix = request.GET.get('unix')
        username = request.user.username
        comment_title = xss(comment_title)

        if comment_title and comment_content:

            from app.models import App_Blog
            from django.contrib.auth.models import User
            from app.utli.datetimenow import datetime_ymd
            a_time = datetime_ymd()
            user = User.objects.get(username=username)

            App_Blog(
                title=comment_title,
                content=comment_content,
                time_add=a_time,
                time_now=a_time,
                username=user,
                tid_unix=comment_unix
            ).save()

            return HttpResponseRedirect('/')

        dic = {
            'title': comment_title,
            'content': comment_content,
            'err': u'不能为空'
        }

        return render(request, 'home/editors.html', dic)


@login_required(login_url='/auth/login/')
@permission_required(perm='app.app_edit_article', login_url='/app/info/')
def edit(request, tid=None):

    if request.method == 'GET':
        unix = request.GET.get('unix')
        print('unix', unix)
        dic = app_index.app_edit_get(request, tid, unix)

        return render(request, 'home/editors.html', dic)

    if request.method == 'POST':
        print('ID', tid)
        #app_index.app_edit_post(request, tid)

        from app.models import App_Blog
        from django.contrib.auth.models import User
        from app.utli.datetimenow import datetime_ymd, datetime_unix

        username = request.user.username

        users = User.objects.get(username=username)

        u_id = users.id

        con = App_Blog.objects.get(id=tid)

        comment_title = request.POST.get('title')
        comment_content = request.POST.get('content')

        from app.utli.xss import xss
        comment_title = xss(comment_title)
        con.title = comment_title
        con.content = comment_content
        con.username = users
        con.save()

        return HttpResponseRedirect('/')


@login_required(login_url='/auth/login/')
@permission_required(perm='app.app_delete_article', login_url='/app/info/')
def delete(request, tid):
    if request.method == 'GET':
        unix = request.GET.get('unix')

        path = ROOT + '/static/upload'
        tid_con = models.App_Blog.objects.get(id=tid)
        tid_user = tid_con.username
        username = request.user.username

        if str(tid_user) == str(username) or user_admin(str(username)):
            from app.utli.rm import rm
            rm(path, unix)
            tid_con.delete()

        return HttpResponseRedirect('/')


def info(request):
    return render(request, 'create.html')
