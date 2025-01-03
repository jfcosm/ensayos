from django import forms
from .models import Rehearsal, Song



class RehearsalForm(forms.ModelForm):
    class Meta:
        model = Rehearsal
        fields = ['date_option_1', 'date_option_2', 'date_option_3', 'location', 'participants', 'songs']
        widgets = {
            'date_option_1': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'date_option_2': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'date_option_3': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'participants': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'songs': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }



class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'lyrics_and_chords']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the title of the song'
            }),
            'lyrics_and_chords': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Paste the lyrics and chords here',
                'rows': 10
            }),
        }


def clean_lyrics_and_chords(self):
    data = self.cleaned_data['lyrics_and_chords']
    if not data.strip():
        raise forms.ValidationError("Este campo no puede quedar vacío.")
    return data
