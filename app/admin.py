# -*- coding: utf-8 -*-
from django.contrib import admin

from account.models import User


class MyAdminSite(admin.AdminSite):
    title = '网站管理后台'
    site_title = title  # 浏览器窗口栏的标题
    site_header = title  # 管理页的标题


class MomentAdmin(admin.ModelAdmin):
    empty_value_display = "空值"
    headline_empty_value_display = "未设置标题"

# UserName Admin job
# PassWord Admin job123.com


# Register your models here.
# admin_site = MyAdminSite()
admin.site.register(User)
