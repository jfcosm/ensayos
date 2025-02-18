from django import forms
from .models import Rehearsal, Song


class RehearsalForm(forms.ModelForm):
    class Meta:
        model = Rehearsal
        fields = [
            'date_option_1', 'time_option_1',
            'date_option_2', 'time_option_2',
            'date_option_3', 'time_option_3',
            'location', 'participants', 'songs'
        ]
        labels = {
            'date_option_1': 'Primera opción de fecha',
            'time_option_1': 'Horario primera opción',
            'date_option_2': 'Segunda opción de fecha',
            'time_option_2': 'Horario segunda opción',
            'date_option_3': 'Tercera opción de fecha',
            'time_option_3': 'Horario tercera opción',
            'location': 'Ubicación',
            'participants': 'Participantes',
            'songs': 'Canciones',
        }
        widgets = {
            'date_option_1': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'time_option_1': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control timepicker'}),
            'date_option_2': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'time_option_2': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control timepicker'}),
            'date_option_3': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'time_option_3': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control timepicker'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la ubicación'}),
            'participants': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'songs': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'lyrics_and_chords']
        labels = {
            'title': 'Título de la canción',
            'lyrics_and_chords': 'Letras y acordes',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el título de la canción'}),
            'lyrics_and_chords': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Pega las letras y acordes acá', 'rows': 10}),
        }

    def clean_lyrics_and_chords(self):
        data = self.cleaned_data.get('lyrics_and_chords', '')
        if not data.strip():
            raise forms.ValidationError("Este campo no puede quedar vacío.")
        return data
