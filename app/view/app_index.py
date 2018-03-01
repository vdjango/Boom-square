#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-26 16:14:31
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from app import models
import markdown
from app.utli import datetimenow
from account.permiss.auth_permissions import user_admin

tids = None
edits = False


def index(request):
    pers = None
    username = None
    auth_logins = False
    cont = models.App_GET_Text_all()

    Inits = 0
    value = []
    len_blog = 0
    time_date = '2018-01-01 00:00:00'
    value_dict = {}

    if request.user.is_authenticated():
        username = request.user.username
        pers = user_admin(str(username))
        auth_logins = True

    for i in cont:
        ids = i.id
        data = datetimenow.datetimenow(i.time_now)
        mark = markdown.markdown(i.content)
        __, number = datetimenow.DateTimes(str(data).split('.')[0])

        if int(Inits) == int(number):
            tid_user = False

            tid_con = models.App_Blog.objects.get(id=ids)
            usern = tid_con.username

            if str(usern) == str(username) or pers:
                tid_user = True

            from app.utli.xss import xss
            # comment_title = xss(comment_content=i.title)
            # comment_content = xss(comment_content=mark)

            comment_title = i.title
            comment_content = mark

            value.append({
                "title": comment_title,
                "content": comment_content,
                "username": str(i.username),
                "time_now": str(data).split('.')[0],
                "id": ids,
                "tid_user": tid_user
            }
            )

            time_date = str(data).split('.')[0]
            # log.d('value.append', 'Add')

        else:

            if int(Inits) == 0:
                len_blog = len(value)

            if time_date != '2018-01-01 00:00:00' and value:
                # log.d('value_dict', 'Add')
                value_dict[str(Inits)] = {
                    'time': time_date,
                    'contents_dicts': value
                }

            value = []
            Inits = int(number)

    if len(value) > 0:
        if time_date != '2018-01-01 00:00:00' and value:
            value_dict[str(Inits)] = {
                'time': time_date,
                'contents_dicts': value
            }

        # print('len_blog', len_blog)
        if int(Inits) == 0:
            len_blog = len(value)

        value = []
        Inits = int(number)

    content = {
        'auth_login': auth_logins,
        'username': str(username),  # 用户名称
        'admin': pers,  # 超级管理员
        'len_blog': len_blog,
        'value_dict': value_dict  # 文章等等
    }

    return content


def app_edit_get(request, tid):
    tid_con = models.App_Blog.objects.get(id=tid)
    tid_user = tid_con.username
    username = request.user.username

    if str(tid_user) == str(username) or user_admin(str(username)):
        title = tid_con.title
        content = tid_con.content
        print('content', content)
        dic = {'tid': tid, 'title': title, 'content': content}
        return dic


def app_edit_post(request, tid):

    app = models.App_Blog.objects.get(id=tid)

    title = request.POST.get('title')
    content = request.POST.get('content')

    from app.utli.xss import xss
    #comment_title = xss(comment_content=title)
    #comment_content = xss(comment_content=content)

    comment_title = title
    comment_content = content

    app.title = comment_title
    app.content = comment_content
    app.save()


def app_del_get(request, tid):
    tid_con = models.App_Blog.objects.get(id=tid)
    tid_user = tid_con.username
    username = request.user.username

    if str(tid_user) == str(username):
        tid_con.delete()
    pass
