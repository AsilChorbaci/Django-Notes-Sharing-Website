import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Template,Context

from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactFormMessage
from notes.models import Category, Note, Images, Comment


def index(request):

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    slider = Note.objects.all()[:3]
    context = {'setting': setting, 'page': 'page', 'category': category, 'slider':slider}
    return render(request,'index.html', context)

def category_notes(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    notes = Note.objects.filter(category_id=id)
    context = {'notes': notes,
               'category': category,
               'categorydata': categorydata}
    return render(request,'notes.html',context)

def note_list(request, id, slug):

    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    notes = Note.objects.filter(category_id=id)
    context = {'notes': notes,
               'category': category,
               'categorydata': categorydata}
    return render(request,'notes.html',context)

def note_details(request,id,slug):
    category = Category.objects.all()
    note = Note.objects.get(pk=id)
    images= Images.objects.filter(note_id=id)
    comment= Comment.objects.filter(note_id=id, status='True')
    context = {'note': note,
               'category': category,
               'images': images,
               'comment': comment}
    return render(request,'note_details.html',context)

def about(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'category': category}
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

def note_search(request):
    if request.method == 'POST':
        form= SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()

            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid ==0:
                notes=Note.objects.filter(title__icontains=query)
            else:
                notes= Note.objects.filter(title__icontains=query, category_id=catid)

            #return HttpResponse(notes)
            context = {'notes': notes,
                       'category': category,
                       }
            return render(request, 'notes.html',context)
    return HttpResponseRedirect('/')

def note_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    notes = Note.objects.filter(title__icontains=q)
    results = []
    for rs in notes:
      note_json = {}
      note_json = rs.title
      results.append(note_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)