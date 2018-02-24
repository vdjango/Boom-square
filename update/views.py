from django.http import HttpResponse, JsonResponse
# Create your views here.
from update.utli.wget import update_wget_main, update_version_get
from update.view.update_view import update_view
import threading
from django.contrib.auth.decorators import login_required
from update.utli.zip import update_main

'''
是否进行更新任务
'''

version = '0.0.0'  # 当前版本号
latest_version = '0.0.0'  # 最新版本
release_url = ''
auth_update = True
number = 0
err = ''


@login_required(login_url='/auth/login/')
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


@login_required(login_url='/auth/login/')
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


@login_required(login_url='/auth/login/')
def update(request):
    if request.method == 'GET':
        global latest_version
        global release_url
        rend, latest_version, release_url, upda = update_view(request, version)
        if upda:
            auth_update = True
        else:
            auth_update = False
            pass

        latest_version = latest_version
        release_url = release_url
        print('latest_version', latest_version, 'release_url', release_url)
        return rend


class PrintThread(threading.Thread):
    def run(self):
        global auth_update
        global err

        get, err = update_wget_main(release_url, 'file.zip')

        if get == False:
            print('下载失败', err)
            err = '下载失败' + str(err)
            return err
            pass

        unzip, rm, move = update_main('file.zip', latest_version)
        if unzip == False:
            print('解压失败', unzip)
            err = '解压失败' + str(unzip)
            return unzip
            pass

        if rm == False:
            print('清理备份失败', rm)
            err = '清理备份失败' + str(rm)
            return rm
            pass

        if move == False:
            print('更新文件失败', move)
            err = '更新文件失败' + str(move)
            return rm
            pass

        auth_update = True
