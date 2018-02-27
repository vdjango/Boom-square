from account.view import auth_login, auth_register
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.


def register_access(request):
    '''
    用户注册验证
    '''
    if request.method == 'GET':
        if request.user.is_authenticated():
            return auth_login.auth_return_home()

        return render(request, 'auth/register.html')

    if request.method == 'POST':
        return auth_register.auth_main(request)

    # return render(request, 'auth/register.html')


def login_access(request):
    '''
    用户登陆密码验证
    '''
    if request.method == 'GET':
        if request.user.is_authenticated():
            return auth_login.auth_return_home()
        else:
            return render(request, 'auth/login.html')

    if request.method == 'POST':
        return auth_login.auth_main(request)


@login_required(login_url='/auth/login/')
def logout_access(request):
    return auth_login.auth_logouts(request)


def get_user_access(request):
    from django.contrib.auth.models import User
    from django.http import HttpResponse

    return HttpResponse('Node')
