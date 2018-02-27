"""Owl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
# from app.admin import admin_site
from django.http import HttpResponseRedirect


# @login_required(login_url='/auth/login/')
def index(request):
    return HttpResponseRedirect('/app/')


urlpatterns = [
    # adminsetup
    url(r'^auth/', include('account.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^app/', include('app.urls')),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^update/', include('update.urls')),
    url(r'^$', index),
]
