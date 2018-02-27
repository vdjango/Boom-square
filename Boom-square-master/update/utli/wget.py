#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-16 14:26:26
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

import requests
from contextlib import closing
from requests import exceptions


line = 99
off = True


class ProgressBar(object):
    def __init__(self, count=0.0, total=100.0, chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.total = total
        self.count = count
        self.chunk_size = chunk_size

    def __get_info(self):
        # self.total/self.chunk_size = 下载包总大小
        totcgunk = self.total / self.chunk_size  # 下载包总大小
        couchunk = self.count / self.chunk_size  # 当前下载了多少
        BFBI = (float(couchunk) / float(totcgunk) * 100)

        return str(BFBI).split('.')[0]

    def refresh(self, count=1, status=None):
        self.count += count

        return self.__get_info()


def update_wget_main(url, filePath='file.zip'):
    NETWORK_STATUS = True
    try:
        session = requests.Session()
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        session.get('https://www.baidu.com/', timeout=2.0)
    except exceptions.ConnectTimeout:
        NETWORK_STATUS = False

    if NETWORK_STATUS == False:
        return False, '网络连接超时或网络不可达'

    return update_version_wget(url, filePath)


def update_version_wget(url, filePath='file.zip'):
    global line
    global off

    chunk_size = 1024
    line = 0

    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    wget = session.get(url, stream=True)

    with closing(wget) as response:
        if response.status_code == 200:
            try:
                content_size = int(response.headers['content-length'])
            except exceptions.Timeout as e:
                print('Timeout', '请求超时')
                return False, 'Timeout 请求超时'
            except exceptions.ConnectTimeout as e:
                print('ConnectTimeout', '网络连接超时或网络不可达')
                return False, 'ConnectTimeout 网络连接超时或网络不可达'

    progress = ProgressBar(total=content_size, chunk_size=chunk_size)

    with open(filePath, "wb") as file:
        for data in response.iter_content(chunk_size=chunk_size):
            file.write(data)
            number = progress.refresh(count=len(data))
            if number != line:
                line = number

    return True, '下载完成'


def update_version_get():
    return line
