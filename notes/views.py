from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from notes.models import CommentForm, Comment


def index(request):
    return HttpResponse("Note index method")


@login_required(login_url='/login')
def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user=request.user
            data=Comment() # model ile bağlantı kur
            data.user_id=current_user.id
            data.note_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate=form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet

            messages.success(request, "Your Review Has Been sent")

            return HttpResponseRedirect(url)
    messages.warning(request,"Your Review Does not received")
    return HttpResponseRedirect(url)