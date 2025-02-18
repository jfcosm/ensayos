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
            messages.success(request, "¡Excelente! Acabas de ingresar una canción en tu setlist")
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
            messages.success(request, "¡Muy bien! Acabas de agendar tu ensayo exitosamente")
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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Rehearsal
from django.db.models import Count
from datetime import datetime
from django.core.exceptions import ValidationError

def select_date(request, rehearsal_id):
    rehearsal = get_object_or_404(Rehearsal, id=rehearsal_id)

    if request.method == "POST":
        selected_datetime = request.POST.get("selected_datetime")

        if selected_datetime:
            # Guardar la votación del usuario en la sesión
            request.session[f'vote_rehearsal_{rehearsal.id}'] = selected_datetime

            # Contabilizar los votos de cada fecha
            vote_counts = {
                rehearsal.date_option_1: 0,
                rehearsal.date_option_2: 0,
                rehearsal.date_option_3: 0
            }

            for key in request.session.keys():
                if key.startswith(f'vote_rehearsal_{rehearsal.id}'):
                    vote = request.session[key]
                    date_part = vote.split(" ")[0]  # Extrae solo la fecha (sin la hora)
                    for option in vote_counts.keys():
                        if str(option) == date_part:
                            vote_counts[option] += 1

            # Determinar la fecha más votada
            selected_final_date = max(vote_counts, key=vote_counts.get)

            # Si todos los participantes han votado, asignar la fecha definitiva
            if len(request.session.keys()) >= rehearsal.participants.count():
                rehearsal.final_date = selected_final_date
                rehearsal.save()
                messages.success(request, f"La fecha definitiva del ensayo es {selected_final_date}")

            else:
                messages.success(request, "Tu elección ha sido guardada. Esperando votos de otros integrantes.")

            return render(request, "rehearsals/select_date_success.html", {"rehearsal": rehearsal})

    return render(request, "rehearsals/select_date.html", {"rehearsal": rehearsal})

from django.shortcuts import render, get_object_or_404
from .models import Song

def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return render(request, 'rehearsals/song_detail.html', {'song': song})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Rehearsal

@login_required
def user_dashboard(request):
    # Obtener los ensayos donde el usuario es participante
    user_rehearsals = Rehearsal.objects.filter(participants=request.user)

    return render(request, "rehearsals/user_dashboard.html", {"user_rehearsals": user_rehearsals})


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente después de registrarse
            return redirect('user_dashboard')
    else:
        form = UserCreationForm()

    return render(request, "rehearsals/register.html", {"form": form})
