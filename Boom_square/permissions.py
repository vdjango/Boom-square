#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-26 10:40:34
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$


from django.core.urlresolvers import resolve
from django.shortcuts import render, redirect


perm_dic = {
    'GET': {
        'app_see_article': ['index', []],
        'app_create_article': ['create', []],
        'app_edit_article': ['edit', []],
        'app_delete_article': ['delete', []],

        'update_see_article': ['update', []],
        'update_see_article': ['version_get', []],
        'update_see_article': ['version_update', []],
    },


    'POST': {
        'app_edit_article': ['edit', []],
        'app_create_article': ['create', []],
    },

    # GET为查询，POST提交数据

}


matched_flag = False


def request_get(request, perm_key, perm_val, url_namespace):
    global matched_flag
    matched_perm_key = None

    if len(perm_val) == 2:
        url_names, request_args = perm_val
        print('url_names', url_names)
        print('url_namespace', url_namespace)
        if url_namespace == url_names:
            if request.method == "GET":
                # 如果权限列表中无请求参数，此时已可以确定找到了权限规则
                if not request_args:
                    matched_flag = True
                    matched_perm_key = perm_key
                    print('matched perm ...')
                    return matched_flag, matched_perm_key
                else:
                    # 如果权限列表中有请求的参数，反射出request中get或post数据
                    request_method_func = getattr(request, 'GET')
                    # 如果权限列表中所有请求参数都与反射出的参数匹配，则证明权限匹配成功
                    for request_arg in request_args:
                        if request_method_func.get(request_arg) is not None:
                            matched_flag = True
                        else:
                            # 一旦有不匹配的情况，则证明权限已经匹配错误，后续无须再做判断
                            # matched_flag = False
                            print("request arg[%s] not matched" % request_arg)
                            return matched_flag, matched_perm_key
                            # 如果此条规则匹配成功，不需要再做后续其它规则的匹配
                            if matched_flag == True:
                                print("--passed permission check --")
                                matched_perm_key = perm_key
                                return matched_flag, matched_perm_key
        else:
            return matched_flag, matched_perm_key


def request_post(request, perm_key, perm_val, url_namespace):
    global matched_flag
    matched_perm_key = None

    if len(perm_val) == 2:
        url_namespace, request_args = perm_val
        if url_namespace == url_namespace:
            if request.method == "POST":
                # 如果权限列表中无请求参数，此时已可以确定找到了权限规则
                if not request_args:
                    matched_flag = True
                    matched_perm_key = perm_key
                    return matched_flag, matched_perm_key
                else:
                    # 如果权限列表中有请求的参数，反射出request中get或post数据
                    request_method_func = getattr(request, 'GET')
                    # 如果权限列表中所有请求参数都与反射出的参数匹配，则证明权限匹配成功
                    for request_arg in request_args:
                        if request_method_func.get(request_arg) is not None:
                            matched_flag = True
                        else:
                            # 一旦有不匹配的情况，则证明权限已经匹配错误，后续无须再做判断
                            # matched_flag = False
                            print("request arg[%s] not matched" % request_arg)
                            return matched_flag, matched_perm_key
                            # 如果此条规则匹配成功，不需要再做后续其它规则的匹配
                            if matched_flag == True:
                                print("--passed permission check --")
                                matched_perm_key = perm_key
                                return matched_flag, matched_perm_key
        else:
            return matched_flag, matched_perm_key


def perm_check(*args, **kwargs):
    request = args[0]
    # 反向解析request中url
    url_resovle_obj = resolve(request.path_info)
    url_namespace = url_resovle_obj.url_name

    matched_flag = False
    matched_perm_key = None
    # 如果正确反解析出了url且其在权限字典中
    if url_namespace is not None:
        if request.method == 'GET':
            for perm_key in perm_dic['GET']:
                perm_val = perm_dic['GET'][perm_key]
                matched_flag, matched_perm_key = request_get(
                    request, perm_key, perm_val, url_namespace)

        if request.method == 'POST':
            for perm_key in perm_dic['GET']:
                perm_val = perm_dic['GET'][perm_key]
                matched_flag, matched_perm_key = request_post(
                    request, perm_key, perm_val, url_namespace)

    else:
        # 如果request解析出的url与urls不匹配，放过？？？
        return True
    # request请求与权限规则已匹配
    if matched_flag == True:
        app = str(request.path_info).split('/')[1]

        perm_str = app + "." + str(matched_perm_key)

        # 如果用户被授与此权限，返回True，否则返回False
        if request.user.has_perm(perm_str):
            print("\033[42;1m ------ 用户具有此权限 %s-------\033[0m" % perm_str)
            return True
        else:
            print("\033[41;1m ------- 用户没有此权限 %s--------\033[0m" % perm_str)
            return False
    else:
        print("\033[41;1m ------ 无效的请求 ----- \033[0m")
        return False


def permission_reques(func):
    def wrapper(*args, **kwargs):
        print("--start check perms", args[0])
        if not perm_check(*args, **kwargs):
            return render(args[0], 'error/403.html')
        return func(*args, **kwargs)
    return wrapper
