#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-14 20:47:07
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

import urllib3
import json


def get_Json(url=None, method='GET', code='utf8'):
    '''
    获取Url Json格式数据
    可选参数：
    url=None json 地址
    method='GET', 请求方法
    code='utf8' 返回数据编码
    '''
    http = urllib3.PoolManager()
    if url:
        url = url  # 'http://shszcraft.com:8080/?format=json'

    else:
        url = 'http://shszcraft.com:9090/?format=json'

    # print('url', url)
    html = http.request('GET', url)
    return json.loads(html.data.decode('utf8'))


def get_update(json):
    '''
    获取更新源
    return list(list)
    '''
    update = json['update']

    return list(update)


def init(version='0.0.0', keys=0):
    json = get_Json()
    yum = get_update(json)

    try:
        dic = yum[keys]
    except Exception as e:
        raise e

    update = get_Json(dic['address'])
    # print(update)

    _version = update["latest_version"]

    MAJOR_update = str(_version).split('.')[0]
    MINOR_update = str(_version).split('.')[1]
    PATCH_update = str(_version).split('.')[2]

    MAJOR_version = str(version).split('.')[0]
    MINOR_version = str(version).split('.')[1]
    PATCH_version = str(version).split('.')[2]

    if MAJOR_version < MAJOR_update:
        return True, update, yum

    if MINOR_version < MINOR_update:
        return True, update, yum

    if PATCH_version < PATCH_update:
        return True, update, yum

    return False, update, yum
    # latest_version

    for x in list(range(10)):
        lis = init()
