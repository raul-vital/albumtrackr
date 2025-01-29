from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('albums/', views.album_index, name='album-index'),
    path('albums/<int:album_id>/', views.album_detail, name='album-detail'),


]