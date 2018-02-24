#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-24 15:06:55
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.contrib.auth.models import Permission, User  # 用户 权限


def user_admin(username):
    param = User.objects.get(username=username).get_all_permissions()

    perm = ['auth.delete_user', 'auth.add_user', 'account.delete_user',
            'account.add_user', 'admin.add_logentry']

    permission = []

    if param != None:
        for line in param:
            for per in perm:
                if line == per:
                    permission.append(line)

    if len(permission) > len(perm) - 3:
        return True

    return False
