#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-07 19:04:06
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.conf.urls import url
from account import views


urlpatterns = [
    url(r'^login/$', views.login_access, name='login'),
    url(r'^register/$', views.register_access, name='register'),
    url(r'^logout/$', views.logout_access, name='logout'),
    url(r'^user/get$', views.get_user_access)
]
