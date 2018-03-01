#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-26 20:46:10
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

import os

import sys
import platform


def set(System, Version):

    install = ['bs4', 'Django==1.10', 'Markdown', 'pytz', 'requests']

    if System == 'Windows':
        for ins in install:
            os.system('pip install ' + str(ins))

        os.system('manage.py makemigrations')
        os.system('manage.py migrate')
        os.system('manage.py createsuperuser')
        print('python3.6 manage.py runserver 0.0.0.0:8080')
        return True

    if Version == '36' or Version == '3.6' or Version == '6':

        for ins in install:
            os.system('pip3.6 install ' + str(ins))

        os.system('python3.6 manage.py makemigrations')
        os.system('python3.6 manage.py migrate')
        os.system('python3.6 manage.py createsuperuser')
        print('python3.6 manage.py runserver 0.0.0.0:8080')
        return True

    if Version == '34' or Version == '3.4' or Version == '4':

        for ins in install:
            os.system('pip3.4 install ' + str(ins))

        os.system('python3.4 manage.py makemigrations')
        os.system('python3.4 manage.py migrate')
        os.system('python3.4 manage.py createsuperuser')
        print('python3.4 manage.py runserver 0.0.0.0:8080')
        return True

    if Version == '30' or Version == '3.0' or Version == '0' or Version == '3':

        for ins in install:
            os.system('pip3 install ' + str(ins))

        os.system('python3 manage.py makemigrations')
        os.system('python3 manage.py migrate')
        os.system('python3 manage.py createsuperuser')
        print('python3 manage.py runserver 0.0.0.0:8080')
        return True


version = sys.version_info
System = platform.system()
ver = '%s.%s' % (version.major, version.minor)

if version < (3, 0):
    print('At least Python 3.0 is required')
    # return False

set(System, ver)
