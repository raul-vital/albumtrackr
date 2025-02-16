from django.shortcuts import render, redirect, get_object_or_404
from .models import Album, Song
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
import requests
from django.conf import settings
import os
from bs4 import BeautifulSoup

YOUTUBE_SEARCH_URL = os.getenv('YOUTUBE_SEARCH_URL')
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
GENIUS_API_URL = "https://api.genius.com/"

class Home(LoginView):
    template_name = 'home.html'

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

@login_required
def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    song_form = SongForm()
    return render(request, 'albums/detail.html', {'album': album, 'song_form': song_form})

# ************************************************
def get_youtube_video(song_title, artist):
    api_key = os.getenv('YOUTUBE_API_KEY')
    search_query = f"{song_title} {artist} official music video"

    params = {
        "part": "snippet",
        "q": search_query,
        "key": api_key,
        "maxResults": 1,
        "type": "video"
    }

    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    data = response.json()
    print(data)

    if "items" in data and len(data["items"]) > 0:
        video_id = data["items"][0]["id"]["videoId"]
        print(video_id)
        return f"https://www.youtube.com/embed/{video_id}"
      
    return None

# ************************************************
@login_required
def song_detail(request, song_id):
    # debug_api_key() 
    song = get_object_or_404(Song, id=song_id)
    youtube_url = get_youtube_video(song.title, song.album.artist)
    lyrics = get_lyrics_from_genius(song.title, song.album.artist)
    print(youtube_url)
    return render(request, 'songs/song_detail.html', {'song': song, 'youtube_url': youtube_url, 'lyrics': lyrics})

@login_required
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

class SongUpdate(LoginRequiredMixin, UpdateView):
    model = Song
    fields = ['title', 'release_date', 'release_country', 'mood', 'lyrics']
    def get_success_url(self):
        song = self.object 
        return f'/albums/{song.album.id}/'

class SongDelete(LoginRequiredMixin,DeleteView):
    model = Song
    def get_success_url(self):
        song = self.object 
        return f'/albums/{song.album.id}/'

# ************************************************
def get_lyrics_from_genius(song_title, artist):
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    params = {"q": f"{song_title} {artist}"}

    response = requests.get(f"{GENIUS_API_URL}search", headers=headers, params=params).json()

    song_url = f"https://genius.com{response.get('response', {}).get('hits', [{}])[0].get('result', {}).get('path', '')}"
    
    return scrape_lyrics(song_url) if song_url else "Lyrics not found."

def scrape_lyrics(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return "Lyrics not available."

    soup = BeautifulSoup(response.text, "html.parser")
    lyrics = "\n".join(div.get_text(separator="\n") for div in soup.select("div[data-lyrics-container='true']"))
    
    return lyrics.strip() or "Lyrics not found."