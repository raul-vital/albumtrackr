from django.shortcuts import render
from .models import Album
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
def home(request):
    return render(request, 'home.html')

def album_index(request):
    albums = Album.objects.all()
    return render(request, 'albums/index.html', {'albums': albums})

def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    return render(request, 'albums/detail.html', {'album': album})

class AlbumCreate(CreateView):
    model = Album
    fields = '__all__'

class AlbumUpdate(UpdateView):
    model = Album
    fields = '__all__'

class AlbumDelete(DeleteView):
    model = Album
    success_url = '/albums/'