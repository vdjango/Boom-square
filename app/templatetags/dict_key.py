#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-12 21:16:53
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django import template
from django.template.defaultfilters import stringfilter
from app.utli import datetimenow

register = template.Library()


@stringfilter
@register.filter(is_safe=True)
def key(d, key_name):
    value = None
    try:
        value = d[key_name]
    except KeyError:
        value = None
    return value


@stringfilter
@register.filter(is_safe=True)
def time_key(d, key=None):
    value = None
    try:
        time_k, __ = datetimenow.DateTimes(str(d))
        if time_k and key == None:
            value = '今日留言'
        else:
            k = str(key).split(':')
            value = str(d).split(" ")[int(k[1])]

    except KeyError:
        value = None
    return value


@stringfilter
@register.filter(is_safe=True)
def time_get(d):
    value = False
    try:
        time_k, __ = datetimenow.DateTimes(str(d))
        if time_k:
            value = True

    except KeyError:
        value = False
    return value
