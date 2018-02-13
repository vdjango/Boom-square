#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-12 11:48:12
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

import pytz
from datetime import datetime
from django.utils.timezone import utc
from Boom_square import settings


def UTCS():
    # datetime.datetime.utcnow().replace(tzinfo=utc)
    # datetime.datetime.strptime('2018-02-11 03:37:43', "%Y-%m-%d %H:%M:%S")

    return datetime.utcnow().replace(tzinfo=utc)


def datetimenow(data=None):
    ZONE = pytz.timezone(settings.TIME_ZONE)
    if data == None:
        data = UTCS()
        print('UTC: ' + str(data))

    time = data.astimezone(ZONE)
    # print(time)
    return time


def DateTimes(date):
    '''
    datetime_from_db = '2015-10-26 00:00:00'
    '''
    datetime_from = datetime.now()

    datetime_of = datetime.strptime(
        date, "%Y-%m-%d %H:%M:%S")

    data_year = str(datetime_of).split(" ")[0].split("-")[0]  # '年'
    data_month = str(datetime_of).split(" ")[0].split("-")[1]  # '月'
    data_day = str(datetime_of).split(" ")[0].split("-")[2]  # '日'
    data_time = str(datetime_of).split(" ")[1].split(":")[0]  # '时'
    data_branch = str(datetime_of).split(" ")[1].split(":")[1]  # '分'
    data_second = str(datetime_of).split(" ")[1].split(":")[2]  # '秒'

    data_for_year = str(datetime_from).split(" ")[0].split("-")[0]  # '年'
    data_for_month = str(datetime_from).split(" ")[0].split("-")[1]  # '月'
    data_for_day = str(datetime_from).split(" ")[0].split("-")[2]  # '日'
    data_for_time = str(datetime_from).split(
        " ")[1].split(".")[0].split(":")[0]  # '时'
    data_for_branch = str(datetime_from).split(
        " ")[1].split(".")[0].split(":")[1]  # '分'
    data_for_second = str(datetime_from).split(
        " ")[1].split(".")[0].split(":")[2]  # '秒'

    date_of = data_year + data_month + data_day
    date_for = data_for_year + data_for_month + data_for_day

    date_of_t = data_time + data_branch + data_second
    date_for_t = data_for_time + data_for_branch + data_for_second

    number = int(date_for) - int(date_of)
    # number_time = int(date_for_t) - int(date_of_t)

    # 240000
    if number < 1 and number > -1:
        return True, number
    else:
        return False, number
