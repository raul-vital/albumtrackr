from django.shortcuts import render, redirect
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

# Create your views here.
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

    
class SongUpdate(LoginRequiredMixin, UpdateView):
    model = Song
    fields = ['title', 'release_date', 'release_country', 'mood', 'lyrics']
    success_url = '/songs/' 


class SongDelete(LoginRequiredMixin, DeleteView):
    model = Song
    success_url = '/songs/' 
