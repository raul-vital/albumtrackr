from django.shortcuts import render, redirect
from .models import Album
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import AlbumForm, Song
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

@login_required
def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    album_form = AlbumForm()
    return render(request, 'albums/detail.html', {'album': album, 'album_form': album_form})

def song_detail(request, song_id):
    song = Song.objects.get(id=song_id)
    song_form = SongForm()
    return render(request, 'songs/detail.html', {'song': song, 'song_form': song_form})
    


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