from django.shortcuts import render
from django.http import HttpResponseRedirect
from update.utli.update import init
# Create your views here.


def update(request):
    mess = ''
    boo, update_, yum = init('0.1.-1')
    latest_version = update_['latest_version']
    up = update_['releases']
    latest_version = up[latest_version]

    if boo:
        mess = '发现可用新版本。'
    else:
        mess = '已更新至最新版本。'

    dic = {
        "boo": boo,
        "mess": mess,
        "yum": yum,
        "update": update_,
        "latest_version": latest_version
    }

    return render(request, 'home/update.html', dic)
