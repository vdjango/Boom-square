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
        url = 'http://shszcraft.com:8080/?format=json'

    html = http.request('GET', url)
    return json.loads(html.data.decode('utf8'))


def get_update(json):
    '''
    获取更新源
    return list(list)
    '''
    update = json['update']

    return list(update)


def update_main():
    json = get_Json(url='http://shszcraft.com:8080/')
    update = get_update(json)
    pass


update_main()
# print(value, ..., sep, end, file, flush)
