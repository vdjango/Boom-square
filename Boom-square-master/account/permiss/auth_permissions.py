#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-24 15:06:55
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.contrib.auth.models import Permission, User, Group  # 用户 权限

PermissionDefault = [
    'app_see_article',
    'app_create_article',
    'app_edit_article',
    'app_delete_article',
    'app_reply_discussion',

]

PermissionAdmin = [
]


def user_admin(username):
    param = User.objects.get(username=username)
    return param.is_staff


def add_group_default(username):
    '''
    如果用户组不存在则创建用户组
    添加用户到用户组
    '''
    global PermissionDefault
    groups = None
    try:
        groups = Group.objects.get(name='default')
        data = {'code': -7, 'info': u'组名已存在'}
    except Group.DoesNotExist:
        groups = Group.objects.create(name='default')

        for perline in PermissionDefault:
            permission = Permission.objects.get(codename=perline)
            groups.permissions.add(permission)

    # user添加组属性
    db_user = User.objects.get(username=username)
    db_user.groups.add(groups)
    data = {'code': 1, 'info': u'添加成功'}


def add_group_admin(username):
    '''
    如果用户组不存在则创建用户组
    添加用户到用户组
    '''
    global PermissionAdmin
    groups = None
    try:
        groups = Group.objects.get(name='admin')
        data = {'code': -7, 'info': u'组名已存在'}
    except Group.DoesNotExist:
        groups = Group.objects.create(name='admin')

        for perline in PermissionDefault:
            permission = Permission.objects.get(codename=perline)
            groups.permissions.add(permission)

    # user添加组属性
    db_user = User.objects.get(username=username)
    db_user.groups.add(groups)
    data = {'code': 1, 'info': u'添加成功'}
