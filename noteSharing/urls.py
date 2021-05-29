"""noteSharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
""" 
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from home import views
from noteSharing import settings

urlpatterns = [
    path('', include('home.urls')),
    path('note/', include('notes.urls')),
    path('home/', include('home.urls')),
    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<int:id>/<slug:slug>/', views.note_list, name='note_list'),
    path('note/<int:id>/<slug>/', views.note_details, name='note_detail'),
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)