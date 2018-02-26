#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-26 20:46:10
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

import os


def setadmin():
    # os.system('pip3.6 install django==1.10')
    # os.system('pip3.6 install markdown')
    # os.system('pip3.6 install uwsgi')
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    os.system('python manage.py runserver 0.0.0.0:8080')

    # print('接下来您要创建您的管理用户')
    # os.system('python manage.py createsuperuser')


setadmin()
