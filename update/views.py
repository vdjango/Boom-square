from django.http import HttpResponse, JsonResponse
# Create your views here.
from update.utli.wget import wget, update_version_get
from update.view.update_view import update_view
import threading
from django.contrib.auth.decorators import login_required, permission_required
from update.utli.zip import update_main
from django.shortcuts import render
from update.models import update
from app.utli.datetimenow import UTCS

'''
是否进行更新任务
'''

version = '0.1.0'  # 当前版本号
latest_version = '0.0.0'  # 最新版本
release_url = ''
auth_update = True  # 开启更新
auth_install = False  # 安装完成
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
        if int(number) >= 95:
            if auth_update:
                if auth_install:
                    number = 100

            else:
                number = 95

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
def updates(request):
    if request.method == 'GET':

        from account.permiss.auth_permissions import user_admin
        per = user_admin(request.user.username)
        if per == False:
            pass
        global latest_version
        global release_url
        global version

        data = UTCS()
        time = "%s-%s-%s %s:%s:%s" % (
            data.year, data.month, data.day,
            data.hour, data.minute, data.second)

        ver = update.objects.all().values('version')

        if not ver:
            update(version=version, time=time).save()
            ver = update.objects.all().values('version')
            pass

        version = ver[0]['version']

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
        global release_url
        global auth_update
        global err
        global version
        global latest_version

        get, err = wget(release_url, 'file.zip')

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
        ver = update.objects.get(version=version)
        ver.version = latest_version
        ver.save()
        auth_install = True


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
