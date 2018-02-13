# -*- coding: utf-8 -*-
from django.contrib import admin

from account.models import User
from app.models import App_Blog


class MyAdminSite(admin.AdminSite):
    title = '网站管理后台'
    site_title = title  # 浏览器窗口栏的标题
    site_header = title  # 管理页的标题


class MomentAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "time_now", "username"]

    # 自定义后台过滤器
    list_filter = ["time_add"]

    # 自定义后台搜索
    search_fields = ["title", "content"]

    class Meta:
        model = App_Blog


# UserName Admin job
# PassWord Admin job123.com


# Register your models here.
# admin_site = MyAdminSite()
admin.site.register(User)
admin.site.register(App_Blog, MomentAdmin)
