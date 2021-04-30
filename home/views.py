from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template,Context

from home.models import Setting


def index(request):

    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request,'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'about.html', context)

def contact(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'contact.html', context)
