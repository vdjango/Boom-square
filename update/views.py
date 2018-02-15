from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.


def update(request):

    return render(request, 'home/update.html')
