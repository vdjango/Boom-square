from django.http import HttpResponse, JsonResponse
# Create your views here.
from update.utli.wget import update_wget_main, update_version_get
from update.view.update_view import update_view
import threading
from django.contrib.auth.decorators import login_required, permission_required
from update.utli.zip import update_main
from django.shortcuts import render

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
@permission_required(perm='update.update_version_get_article', login_url='/update/info/')
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
@permission_required(perm='update.update_version_update_article', login_url='/update/info/')
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
@permission_required(perm='update.update_update_article', login_url='/update/info/')
def update(request):
    if request.method == 'GET':

        from account.permiss.auth_permissions import user_admin
        per = user_admin(request.user.username)
        if per == False:
            pass
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


def info(request):
    from account.permiss import auth_permissions
    pers = None
    username = None
    auth_logins = False

    if request.user.is_authenticated():
        username = request.user.username
        pers = auth_permissions.user_admin(str(username))
        auth_logins = True

    content = {
        'auth_login': auth_logins,
        'username': str(username),  # 用户名称
        'admin': pers,  # 超级管理员
    }

    return render(request, 'error/403.html', content)
