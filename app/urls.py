#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-05 19:01:27
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.user_home, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/([0-9]+)/$', views.edit, name='edit_post'),
    url(r'^edit/$', views.edit, name='edit_get'),
    url(r'^edit/([0-9]+)/$', views.edit, name='edit'),
    url(r'^delete/([0-9]+)/$', views.delete, name='delete'),
    url(r'^info/$', views.info, name='info'),

]
