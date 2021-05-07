from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Template,Context

from home.models import Setting, ContactForm, ContactFormMessage
from notes.models import Category


def index(request):

    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request,'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'about.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.phone = form.cleaned_data['phone']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Your Message Has Been Sent, Thank You')
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    category = Category.objects.all()
    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'contact.html', context)