from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from home import views
from noteSharing import settings
from user import views as UserViews

urlpatterns = [
    path('', include('home.urls')),
    path('note/', include('notes.urls')),
    path('home/', include('home.urls')),
    path('user/', include('user.urls')),
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<int:id>/<slug:slug>/', views.note_list, name='note_list'),
    path('notes/', views.note_list2, name='note_list2'),
    path('note/<int:id>/<slug>/', views.note_details, name='note_detail'),
    path('search/', views.note_search, name="note_search"),
    path('search-auto/', views.note_search_auto, name="note_search"),
    path('login/', UserViews.login_form, name="login_form"),
    path('logout/', UserViews.logout_fun, name="logout_fun"),
    path('register/', UserViews.register_form, name="register_form"),
    path('faq/', UserViews.faq, name="faq"),
    path('downloadpdf//uploads/images/<filename>', views.download_pdf_file_home, name='download_pdf_file_home'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)