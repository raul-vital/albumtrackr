from django import forms
from .models import Album, Song
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'genres', 'release_date']
        widgets = {
            'release_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date',
                }
            ),
        }

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'release_date', 'release_country', 'mood', 'lyrics']
        widgets = {
                'release_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date',
                }
            ),
        }

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
