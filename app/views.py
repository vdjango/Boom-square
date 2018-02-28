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


def user_home(request):
    if request.method == 'GET':
        content = app_index.index(request)
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

        content = {
            'auth_login': auth_logins,
            'username': str(username),  # 用户名称
            'admin': pers,  # 超级管理员
        }

        return render(request, 'home/editors.html', content)

    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        username = request.user.username

        from app.utli.xss import xss
        comment_title = xss(comment_content=title)
        comment_content = xss(comment_content=content)

        if comment_title and comment_content:
            models.App_SAVE_Text(username, comment_title, comment_content)

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
        dic = app_index.app_edit_get(request, tid)
        return render(request, 'home/editors.html', dic)

    if request.method == 'POST':
        print('ID', tid)
        app_index.app_edit_post(request, tid)

        return HttpResponseRedirect('/')


@login_required(login_url='/auth/login/')
@permission_required(perm='app.app_delete_article', login_url='/app/info/')
def delete(request, tid):
    if request.method == 'GET':
        tid_con = models.App_Blog.objects.get(id=tid)
        tid_user = tid_con.username
        username = request.user.username

        if str(tid_user) == str(username) or user_admin(str(username)):
            print('删除', tid_user, '==', username)
            tid_con.delete()

        return HttpResponseRedirect('/')


def info(request):
    return render(request, 'create.html')
