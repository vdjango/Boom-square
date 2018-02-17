#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-16 14:26:26
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

line = 0


class ProgressBar(object):
    def __init__(self, count=0.0,  total=100.0, chunk_size=1.0):
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

    # url = "https://github.com/ShszCraft/Boom-square/archive/v0.0.0.zip"
    wget = requests.get(url, stream=True)

    chunk_size = 1024

    global line

    with closing(wget) as response:

        if response.status_code == 200:

            content_size = int(response.headers['content-length'])
            """
            需要根据 response.status_code 的不同添加不同的异常处理
            print('content_size', content_size, response.status_code,)
            """
            progress = ProgressBar(total=content_size, chunk_size=chunk_size)

            with open('./file.zip', "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    number = progress.refresh(count=len(data))
                    if number != line:
                        line = number
                        print('下载', line)

            print('下载完成', )


def update_get():
    print('line', line)
    return line
