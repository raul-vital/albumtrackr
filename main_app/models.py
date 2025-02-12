from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genres = models.CharField()
    release_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('album-detail', kwargs={'album_id': self.id})


class Song(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField(max_length=100)
    release_country = models.CharField(max_length=100)
    mood = models.CharField(max_length=100)
    lyrics = models.TextField()

    def __str__(self):
        return f"Song by {self.album.artist} on {self.album.title}"  

    def get_absolute_url(self):
        return reverse('song-detail', kwargs={'pk': self.id})
