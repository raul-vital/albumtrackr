from django.shortcuts import render
from .models import Album

# Create your views here.
def home(request):
    return render(request, 'home.html')

def album_index(request):
    albums = Album.objects.all()
    return render(request, 'albums/index.html', {'albums': albums})

def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    return render(request, 'albums/detail.html', {'album': album})