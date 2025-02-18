from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    lyrics_and_chords = models.TextField(verbose_name="Lyrics and Chords", default='')

    def __str__(self):
        return self.title





class Rehearsal(models.Model):
    date_option_1 = models.DateField(verbose_name="Primera opción de fecha")
    time_option_1 = models.TimeField(verbose_name="Horario primera opción", null=True, blank=True)
    
    date_option_2 = models.DateField(verbose_name="Segunda opción de fecha", null=True, blank=True)
    time_option_2 = models.TimeField(verbose_name="Horario segunda opción", null=True, blank=True)
    
    date_option_3 = models.DateField(verbose_name="Tercera opción de fecha", null=True, blank=True)
    time_option_3 = models.TimeField(verbose_name="Horario tercera opción", null=True, blank=True)

    location = models.CharField(max_length=255, verbose_name="Ubicación")
    participants = models.ManyToManyField("auth.User", verbose_name="Participantes")
    songs = models.ManyToManyField("Song", verbose_name="Canciones")
    
    final_date = models.DateField(null=True, blank=True, verbose_name="Fecha definitiva")

    def __str__(self):
        return f"Ensayo en {self.location} el {self.final_date or 'Fecha por definir'}"
