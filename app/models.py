# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


def App_GET_Text_all():
    t = App_Blog.objects.all()

    return t


def App_GET_Text():
    usernames = User.objects.get(username='1748011755')
    text = App_Blog.objects.get(username=usernames)
    return text


def App_SAVE_Text(username, title, content, time_now=None):
    from app.utli.datetimenow import UTCS

    data = UTCS()
    times = "%s-%s-%s %s:%s:%s" % (data.year, data.month,
                                   data.day, data.hour, data.minute, data.second)

    usernames = User.objects.get(username=username)

    if time_now == None:
        App_b = App_Blog(title=title, content=content,
                         time_add=times, time_now=times, username=usernames)

    else:
        App_b = App_Blog(title=title, content=content,
                         time_now=time_now, username=usernames)

    App_b.save()

    return times


def archive():
    # datetimes() 方法返回一个 python 的 datetimes 对象列表
    # 对应着每篇文章的发表时间
    # month 表示精确到月份，DESC 表示降序排列
    dates = App_Blog.objects.datetimes('time_now', 'month', order='DESC')
    return dates


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
    time_add = models.DateTimeField(auto_now=False)  # 创建
    time_now = models.DateTimeField(auto_now=True)  # 更新
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    tid_unix = models.CharField(max_length=14)

    class Meta:
        ordering = ['-time_now']
        permissions = (
            ("app_see_article", "访问视图权限"),
            ("app_create_article", "创建留言权限"),
            ("app_edit_article", "编辑留言权限"),
            ("app_delete_article", "删除留言权限"),
            ("app_reply_discussion", "评论留言权限"),
        )
