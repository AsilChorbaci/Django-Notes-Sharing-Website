from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template,Context

def index(request):
    return render(request,"index.html")
