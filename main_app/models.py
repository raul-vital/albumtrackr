from django.db import models
from django.urls import reverse

# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genres = models.CharField()
    release_date = models.DateField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('album-detail', kwargs={'album_id': self.id})