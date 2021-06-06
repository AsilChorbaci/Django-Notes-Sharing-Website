from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('addcomment/<int:id>', views.addcomment,name='addcomment')
    path('update/', views.user_update, name='ser_update'),
    path('password/', views.change_password, name='change_password'),
]