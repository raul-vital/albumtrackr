from django.shortcuts import render
from .models import Album
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import AlbumForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def album_index(request):
    albums = Album.objects.all()
    return render(request, 'albums/index.html', {'albums': albums})

def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    album_form = AlbumForm()
    return render(request, 'albums/detail.html', {'album': album, 'album_form': album_form})

class AlbumCreate(CreateView):
    model = Album
    form_class = AlbumForm

class AlbumUpdate(UpdateView):
    model = Album
    fields = '__all__'

class AlbumDelete(DeleteView):
    model = Album
    success_url = '/albums/'