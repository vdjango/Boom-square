from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from update.utli.update import init
# Create your views here.
from update.utli.wget import update_version_wget, update_version_get
from update.view.update_view import update_view
import threading

'''
是否进行更新任务
'''
auth_update = True
number = 0


def version_get(request):
    '''
    获取更新下载进度
    '''
    if request.method == 'GET':
        global number
        number = update_version_get()
        print('number', number)
        if int(number) >= 98:
            if auth_update:
                number = 100
            else:
                number = 98

        print('number', number)
        return JsonResponse(number, safe=False)


def version_update(request):
    '''
    开启线程进行更新
    '''
    if request.method == 'GET':
        global auth_update
        if auth_update:
            prints = PrintThread()
            prints.start()
            auth_update = False
            return HttpResponse('yes')

        return HttpResponse('no')


def update(request):
    if request.method == 'GET':
        return update_view(request)


class PrintThread(threading.Thread):
    def run(self):
        update_version_wget(
            'https://github.com/ShszCraft/Boom-square/archive/v0.0.0.zip')
        from update.utli.zip import update_zip
        update_zip()
        auth_update = True
