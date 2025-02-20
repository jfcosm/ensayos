from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Band, Rehearsal, Song


class CustomUserCreationForm(UserCreationForm):
    band = forms.ModelChoiceField(
        queryset=Band.objects.all(), 
        required=False, 
        label="Selecciona tu banda (o crea una nueva)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    new_band = forms.CharField(
        required=False, 
        label="O ingresa una nueva banda",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la nueva banda'})
    )

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "band", "new_band")

    def clean(self):
        cleaned_data = super().clean()
        band = cleaned_data.get("band")
        new_band = cleaned_data.get("new_band")

        if not band and not new_band:
            raise forms.ValidationError("Debes seleccionar una banda o ingresar un nuevo nombre.")

        return cleaned_data


class RehearsalForm(forms.ModelForm):
    class Meta:
        model = Rehearsal
        fields = [
            'date_option_1', 'time_option_1',
            'date_option_2', 'time_option_2',
            'date_option_3', 'time_option_3',
            'location', 'songs'
        ]
        widgets = {
            'date_option_1': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'time_option_1': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control timepicker'}),
            'date_option_2': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'time_option_2': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control timepicker'}),
            'date_option_3': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'time_option_3': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control timepicker'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación'}),
            'songs': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'lyrics_and_chords']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'lyrics_and_chords': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
