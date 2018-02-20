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
    url(r'^version_get/$', views.version_get,
        name='version_get'),  # 处理数据的url, 当前页面的地址
    url(r'^version_update/$', views.version_update, name='version_update')



]
