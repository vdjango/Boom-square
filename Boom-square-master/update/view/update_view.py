#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 12:29:56
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.shortcuts import render
from update.utli.update import init
from account.permiss.auth_permissions import user_admin


def update_view(request, Version):
    mess = ''
    Upda = False
    boo, update_, yum = init(Version)
    latest_version = update_['latest_version']
    releases = update_['releases']
    VersionDict = releases[latest_version]
    url = VersionDict['release_url']

    if request.user.is_authenticated():
        username = request.user.username
        pers = user_admin(str(username))

    if boo:
        mess = '发现可用新版本。'
        Upda = True
    else:
        mess = '已更新至最新版本。'
        Upda = False

    dic = {
        "username": str(username),  # 用户名称
        "admin": pers,  # 超级管理员
        "boo": boo,
        "mess": mess,
        "yum": yum,
        "update": update_,
        "Version": Version,
        "latest_version": VersionDict
    }

    return render(request, 'home/update.html', dic), latest_version, url, Upda
