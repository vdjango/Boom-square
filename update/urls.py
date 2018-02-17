#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-14 20:17:29
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.conf.urls import url
from update import views

urlpatterns = [
    url(r'^$', views.update, name='user'),
    url(r'^auth_version_get/$', views.auth_version_get,
        name='processss'),  # 处理数据的url, 当前页面的地址
    url(r'^auth_version/$', views.auth_version,
        name='process'),  # 处理数据的url, 当前页面的地址


]
