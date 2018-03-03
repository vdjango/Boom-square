#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-03 23:13:28
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

import os
import shutil


def rm(path, unix):
    for f in os.listdir(path):
        rmfile = os.path.join(path, f)
        rmrf = rmfile + '/' + unix
        if os.path.isdir(rmfile):
            try:
                for root, dirs, files in os.walk(rmrf):
                    for name in files:
                        del_file = os.path.join(root, name)
                        os.remove(del_file)

                    if os.path.exists(rmrf):
                        shutil.rmtree(rmrf)

            except Exception as e:
                raise e
