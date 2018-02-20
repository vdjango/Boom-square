#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-16 14:26:26
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

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


def update_version_wget(url):
    import requests
    from contextlib import closing

    chunk_size = 1024

    global line
    global off

    line = 0

    with closing(requests.get(url, stream=True)) as response:

        if response.status_code == 200:

            try:
                content_size = int(response.headers['content-length'])
            except Exception as e:
                print('Exception', 'Error headers')
                if off:
                    update_version_wget(url)
                    off = False

            progress = ProgressBar(total=content_size, chunk_size=chunk_size)

            with open('./file.zip', "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    number = progress.refresh(count=len(data))
                    if number != line:
                        line = number


def update_version_get():
    return line
