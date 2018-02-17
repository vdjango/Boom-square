from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from update.utli.update import init
# Create your views here.
from update.utli.wget import update_version_wget, update_get


def test(request):
    return render(request, 'home/test.html')
    pass


num_progress = 0  # 当前的后台进度值（不喜欢全局变量也可以很轻易地换成别的方法代替）


def auth_version_get(request):
    a = update_get()
    print(a)
    return JsonResponse(a, safe=False)


# 通过thread 实现django中
import threading
import time


class PrintThread(threading.Thread):
    def run(self):
        print("start....", self.getName())
        global num_progress

        ur = update_version_wget(
            'https://github.com/ShszCraft/Boom-square/archive/v0.0.0.zip')

        print("end....", self.getName())


def auth_version(request):
    if request.method == 'POST':
        content = request.POST.get('name')
        return HttpResponse('1')
    else:
        content = request.GET.get('name')
        prints = PrintThread()
        prints.start()

    return HttpResponseRedirect('/update/')


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
