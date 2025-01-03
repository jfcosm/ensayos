from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    lyrics_and_chords = models.TextField(verbose_name="Lyrics and Chords", default='')

    def __str__(self):
        return self.title

class Rehearsal(models.Model):
    date_option_1 = models.DateTimeField(verbose_name="Date and Time Option 1")
    date_option_2 = models.DateTimeField(verbose_name="Date and Time Option 2", blank=True, null=True)
    date_option_3 = models.DateTimeField(verbose_name="Date and Time Option 3", blank=True, null=True)
    selected_date = models.DateTimeField(verbose_name="Selected Date and Time", blank=True, null=True)
    location = models.CharField(max_length=200, verbose_name="Location")
    participants = models.ManyToManyField(User, related_name='rehearsals', verbose_name="Participants")
    songs = models.ManyToManyField('Song', related_name='rehearsals', verbose_name="Songs")

    def __str__(self):
        return f"Rehearsal Options: {self.date_option_1}, {self.date_option_2}, {self.date_option_3}"
