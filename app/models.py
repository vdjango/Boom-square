# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import json


def App_GET_Text_all():
    t = App_Blog.objects.all()
    return t


def App_GET_Text():
    text = App_Blog.objects.get(username='1748011755')
    return text


def App_SAVE_Text(username, title, content, time_now=None):
    import time
    times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    usernames = User.objects.get(username=username)

    if not time_now:
        App_b = App_Blog(title=title, content=content,
                         time_add=times, time_now=times, username=usernames)
    else:
        App_b = App_Blog(title=title, content=content,
                         time_now=time_now, username=usernames)

    App_b.save()


class App_Blog(models.Model):
    '''
    title 标题
    content 正文
    time_add  创建时间
    time_now 更新时间
    username 发布者 外键
    '''
    title = models.CharField(max_length=64)
    content = models.TextField()
    time_add = models.DateTimeField(auto_now=False, auto_now_add=True)  # 创建
    time_now = models.DateTimeField(auto_now=True, auto_now_add=False)  # 更新
    username = models.ForeignKey(User)

    def __str__(self):
        return self.username
