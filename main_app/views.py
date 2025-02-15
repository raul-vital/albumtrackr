from django.shortcuts import render, redirect, get_object_or_404
from .models import Album
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import AlbumForm, SongForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomLoginForm
from main_app.authentication import EmailOrUsernameModelBackend 
import os
from django.views.generic import TemplateView
from .forms import ApiForm
from .models import Api
import requests
from django import template


YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = os.getenv("YOUTUBE_SEARCH_URL")

# Create your views here.
class Home(LoginView):
    template_name = 'home.html'





def api_view(request):
    """Handles form submission and fetches YouTube videos"""
    videos = {}  # Store video IDs mapped to API titles

    if request.method == 'POST':
        form = ApiForm(request.POST)
        if form.is_valid():
            api_entry = form.save()
            return redirect('api')  # Refresh page after submission

    else:
        form = ApiForm()

    # Retrieve all stored API entries
    api_entries = Api.objects.all()

    # Fetch YouTube videos for each API entry
    for entry in api_entries:
        query = entry.title  # Use stored title for search
        params = {
            "part": "snippet",
            "q": query,
            "key": YOUTUBE_API_KEY,
            "maxResults": 1,  # Fetch only 1 video per title
            "type": "video"
        }

        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        data = response.json()

        if "items" in data and data["items"]:
            video_id = data["items"][0]["id"]["videoId"]
            videos[entry.title] = video_id
    print(videos)
    return render(request, 'api.html', {'form': form, 'api_entries': api_entries, 'videos': videos})


class Login(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='main_app.authentication.EmailOrUsernameModelBackend')
            return redirect('album-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = RegistrationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

@login_required
def album_index(request):
    albums = Album.objects.filter(user=request.user)
    return render(request, 'albums/index.html', {'albums': albums})

# @login_required
# def album_detail(request, album_id):
#     album = Album.objects.get(id=album_id)
#     album_form = AlbumForm()
#     return render(request, 'albums/detail.html', {'album': album, 'album_form': album_form})

@login_required
def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    song_form = SongForm()
    return render(request, 'albums/detail.html', {'album': album, 'song_form': song_form})

def song_detail(request, song_id):
    song = Song.objects.get(id=song_id)
    comment_form = CommentForm()
    return render(request, 'songs/detail.html', {'song': song, 'album_form': slbum_form})
    
def add_song(request, album_id):
    form = SongForm(request.POST)
    if form.is_valid():
        new_song = form.save(commit=False)
        new_song.album_id = album_id
        new_song.save()
    return redirect('album-detail', album_id=album_id)


class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
 
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
    




class AlbumUpdate(LoginRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm

class AlbumDelete(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = '/albums/'