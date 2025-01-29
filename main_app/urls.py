from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('albums/', views.album_index, name='album-index')


]