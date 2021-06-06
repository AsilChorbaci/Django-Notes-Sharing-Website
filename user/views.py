from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from notes.models import Category, Note
from user.forms import SignUpForm
from user.models import UserProfile


def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(pk=current_user.id)
    context= {'category': category,
              'profile': profile}
    return render(request, 'user_profile.html',context)


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, " Login Error")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request,'login.html',context)


def register_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.jpg"
            data.save()
            messages.success(request, "Registration Completed Successfully")
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }

    return render(request, 'register.html', context)


def logout_fun(request):
    logout(request)
    return HttpResponseRedirect('/')