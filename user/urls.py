#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-07 16:39:02
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$


from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^$', views.user_home, name='user'),

]
