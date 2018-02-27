#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-16 14:26:26
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

import requests
from contextlib import closing
from requests import exceptions


import requests
from contextlib import closing
from requests import exceptions


down_line = 0


class ProgressBar(object):
    def __init__(self, count=0.0, total=100.0, chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.total = total
        self.count = count
        self.chunk_size = chunk_size

    def __get_info(self):
        totcgunk = self.total / self.chunk_size
        couchunk = self.count / self.chunk_size
        BFBI = (float(couchunk) / float(totcgunk) * 100)

        return str(BFBI).split('.')[0]

    def refresh(self, count=1, status=None):
        self.count += count
        info = self.__get_info()
        print('Date ', info)
        return info


def wget(url, filePath='file.zip'):
    global down_line
    # url = 'http://p007jqhy3.bkt.clouddn.com/Boom-square-0.1.1.zip'
    try:
        wget = requests.get(url=url, stream=True, )

        with closing(wget) as response:
            chunk_size = 1024
            if response.status_code == 200:
                content_size = int(response.headers['content-length'])

                progress = ProgressBar(
                    total=content_size, chunk_size=chunk_size)

                with open(filePath, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        down_line = progress.refresh(count=len(data))

        return True, '下载完成'

    except Exception as e:

        return False, '下载失败'


def update_version_get():
    return down_line
