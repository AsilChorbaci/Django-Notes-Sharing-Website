from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('addcomment/<int:id>', views.addcomment,name='addcomment')
    path('update/', views.user_update, name='ser_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('notes/', views.notes, name="notes"),
    path('addnote/', views.addnote, name='addnote'),
    path('notedelete/<int:id>', views.notedelete, name='notedelete'),
    path('noteedit/<int:id>', views.noteedit, name='noteedit'),
]