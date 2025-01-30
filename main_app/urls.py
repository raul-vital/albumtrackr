from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('albums/', views.album_index, name='album-index'),
    path('albums/<int:album_id>/', views.album_detail, name='album-detail'),
    path('albums/create/', views.AlbumCreate.as_view(), name='album-create'),
    path('albums/<int:pk>/update', views.AlbumUpdate.as_view(), name='album-update'),
    path('albums/<int:pk>/delete', views.AlbumDelete.as_view(), name='album-delete'),

    


]