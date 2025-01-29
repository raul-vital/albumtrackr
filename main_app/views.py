from django.shortcuts import render
from .models import Album

# Create your views here.
def home(request):
    return render(request, 'home.html')

def album_index(request):
    albums = Album.objects.all()
    return render(request, 'albums/index.html', {'albums': albums})