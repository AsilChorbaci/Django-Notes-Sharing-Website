import mimetypes
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from home.models import Setting, FAQ
from notes.models import Category, Note, Comment, NoteForm, Images, NoteImageForm
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(pk=current_user.id)
    context= {'setting': setting,
              'category': category,
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



def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile Has Been Updated')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        current_user = request.user
        profile = UserProfile.objects.get(pk=current_user.id)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'profile':profile
        }
        return render(request, 'user_update.html', context)



def change_password(request):
    if request.method=='POST':
        form =PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your Password Has Been Changed')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please Fix These Problems<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form =PasswordChangeForm(request.user)
        return render(request,'change_password.html', {
            'form': form, 'category': category
        })


@login_required(login_url='/login')
def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comment.html', context)


@login_required(login_url='/login')
def deletecomment(request, id):
    current_user =request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment Has Been Deleted')
    return HttpResponseRedirect('/user/comments')


def faq(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('notenumber')
    context = {'category': category,
               'faq': faq,
               'setting': setting,
               }
    return render(request, 'faq.html', context)




@login_required(login_url='/login')
def addnote(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Note()
            data.user_id = current_user.id
            data.category = form.cleaned_data['category']
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.file = form.cleaned_data['file']
            data.detail = form.cleaned_data['detail']
            data.slug = form.cleaned_data['slug']
            data.status = 'False'
            data.save()
            messages.success(request, 'Your Content Insterted Successfuly')
            return HttpResponseRedirect('/user/notes')
        else:
            messages.success(request, 'Note Form Error:' + str(form.errors))
            return HttpResponseRedirect('/user/addnote')
    else:
        category = Category.objects.all()
        form = NoteForm()
        context = {
            'category': category,
            'form': form,
            'setting': setting,
        }
        return render(request, 'user_addnote.html', context)

@login_required(login_url='/login')  # Check login
def noteedit(request, id):
    setting = Setting.objects.get(pk=1)
    note = Note.objects.get(id=id)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Note Updated Successfuly')
            return HttpResponseRedirect('/user/notes')
        else:
            messages.success(request, 'Product Form Error: ' + str(form.errors))
            return HttpResponseRedirect('/user/addnote/' + str(id))
    else:
        category = Category.objects.all()
        form = NoteForm(instance=note)
        context = {
            'category': category,
            'form': form,
            'setting': setting,
        }
        return render(request, 'user_addnote.html', context)

@login_required(login_url='/login')  # Check login
def notedelete(request, id):
    current_user = request.user
    Note.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Note deleted...')
    return HttpResponseRedirect('/user/notes')


@login_required(login_url='/login')  # Check login
def notes(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    note = Note.objects.filter( user_id= current_user.id)
    context = {
        'category': category,
        'note': note,
        'setting': setting,
    }
    return render(request, 'user_notes.html', context)



def noteaddimage(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = NoteImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.note_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been successfuly uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error: ' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        note = Note.objects.get(id=id)
        images = Images.objects.filter(note_id=id)
        form = NoteImageForm()
        context = {
            'note': note,
            'images': images,
            'form': form,
        }
        return render(request, 'note_gallery.html', context)


# Define function to download pdf file using template
def download_pdf_file(request, filename):
    category = Category.objects.all()
    context = {'category': category,}
    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/uploads/images/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        # Load the template
        return HttpResponseRedirect('/user/notes')
        #return render(request, 'user_notes.html', context)