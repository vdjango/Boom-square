from django.shortcuts import render
from app.models import App_GET_Text_all
from django.contrib.auth.decorators import login_required
import markdown
from app.utli import datetimenow


class log():
    def d(l, arg):
        print('Log.d:', l, arg)
        pass
