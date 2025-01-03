from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Song, Rehearsal
from .forms import SongForm, RehearsalForm


def home(request):
    return render(request, 'rehearsals/home.html')


# View to create a new song
def create_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Song created successfully!")
            return redirect('song_list')
    else:
        form = SongForm()
    return render(request, 'rehearsals/create_song.html', {'form': form})

# View to list all songs
def song_list(request):
    songs = Song.objects.all()
    return render(request, 'rehearsals/song_list.html', {'songs': songs})

# View to create a new rehearsal

def create_rehearsal(request):
    if request.method == 'POST':
        form = RehearsalForm(request.POST)
        if form.is_valid():
            rehearsal = form.save(commit=False)
            rehearsal.save()
            # Relacionar las canciones seleccionadas con el ensayo
            selected_songs = request.POST.getlist('songs')
            rehearsal.songs.set(selected_songs)
            rehearsal.save()
            messages.success(request, "Rehearsal scheduled successfully!")
            return redirect('rehearsal_list')
    else:
        form = RehearsalForm()

    # Pasar canciones al contexto
    songs = Song.objects.all()
    return render(request, 'rehearsals/create_rehearsal.html', {'form': form, 'songs': songs})


# View to list all rehearsals
def rehearsal_list(request):
    rehearsals = Rehearsal.objects.all()
    return render(request, 'rehearsals/rehearsal_list.html', {'rehearsals': rehearsals})

# View to display rehearsal details and allow date selection
def rehearsal_detail(request, rehearsal_id):
    rehearsal = get_object_or_404(Rehearsal, id=rehearsal_id)
    return render(request, 'rehearsals/rehearsal_detail.html', {'rehearsal': rehearsal})

# View to select the final date for a rehearsal


from datetime import datetime
from django.core.exceptions import ValidationError

def select_date(request, rehearsal_id):
    rehearsal = get_object_or_404(Rehearsal, id=rehearsal_id)
    if request.method == 'POST':
        selected_option = request.POST.get('selected_date')
        if selected_option:
            try:
                # Convierte la fecha seleccionada a un objeto datetime
                parsed_date = datetime.strptime(selected_option, "%Y-%m-%d %H:%M:%S")
                rehearsal.selected_date = parsed_date
                rehearsal.save()
                messages.success(request, "Date selected successfully!")
                return redirect('rehearsal_list')
            except ValueError:
                messages.error(request, "Invalid date format. Please try again.")
    return render(request, 'rehearsals/select_date.html', {'rehearsal': rehearsal})

