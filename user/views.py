from django.shortcuts import render
from app.models import App_GET_Text_all
from django.contrib.auth.decorators import login_required
import markdown


def DateTimes(datetime_from_db):
    from datetime import datetime
    '''
    datetime_from_db = '2015-10-26 00:00:00'
    '''
    datetime_of_datetime_from_db = datetime.strptime(
        datetime_from_db, "%Y-%m-%d %H:%M:%S")
    delta_time = datetime.now() - datetime_of_datetime_from_db
    if delta_time.days <= 0:
        return True
    else:
        return False


@login_required(login_url='/auth/login/')
def user_home(request):
    t = App_GET_Text_all()
    content_list = []
    time_list = []
    T = False

    for i in t:
        print(str(i.time_now).split('.')[0].split(' ')[1])
        if DateTimes(str(i.time_now).split('.')[0]):
            tis = str(i.time_now).split('.')[0].split(' ')[1]
            T = True
        else:
            tis = i.time_now
            T = False

        time_list.append({'time_now': tis, 'T': T})

        mark = markdown.markdown(i.content)

        content_list.append(
            {'title': i.title, 'content': mark,
                'username': i.username, 'time_now': tis, 'T': T}
        )

    content = {'username': request.user.username,
               'content_list': content_list, 'time_list': time_list}
    return render(request, 'home/home.html', content)
