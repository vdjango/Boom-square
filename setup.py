#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-26 20:46:10
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

import os


def setadmin():

    Version = input('请输入您当前的python版本号：')
    if Version == '36' or Version == '3.6' or Version == '6':
        os.system('python3.6 manage.py makemigrations')
        os.system('python3.6 manage.py migrate')
        print('接下来您要创建您的管理用户')
        os.system('python3.6 manage.py createsuperuser')
        print('接下来你可以通过命令启动web了： ', '建议使用screen [yum install screen]')
        print('python3.6 manage.py runserver 0.0.0.0:8080')
        return True

    if Version == '34' or Version == '3.4' or Version == '4':
        os.system('python3.4 manage.py makemigrations')
        os.system('python3.4 manage.py migrate')
        print('接下来您要创建您的管理用户')
        os.system('python3.4 manage.py createsuperuser')
        print('接下来你可以通过命令启动web了： ', '建议使用screen [yum install screen]')
        print('python3.4 manage.py runserver 0.0.0.0:8080')
        return True

    if Version == '30' or Version == '3.0' or Version == '0' or Version == '3':
        os.system('python3 manage.py makemigrations')
        os.system('python3 manage.py migrate')
        print('接下来您要创建您的管理用户')
        os.system('python3 manage.py createsuperuser')
        print('接下来你可以通过命令启动web了： ', '建议使用screen [yum install screen]')
        print('python3 manage.py runserver 0.0.0.0:8080')
        return True

    print('使用方法： ', 'python setup.py [Python版本号]')
    print('如： ', 'python setup.py 3.6')
    print('如： ', 'python setup.py 3.4')
    print('如： ', 'python setup.py 3')


setadmin()
