from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import Song, Rehearsal, CustomUser, Band
from .forms import SongForm, RehearsalForm, CustomUserCreationForm

from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
    return render(request, 'rehearsals/home.html')



def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Verificar si el usuario seleccionó una banda existente o creó una nueva
            selected_band = form.cleaned_data.get("band")
            new_band_name = form.cleaned_data.get("new_band")

            if new_band_name:
                band, created = Band.objects.get_or_create(name=new_band_name)
                user.band = band
            else:
                user.band = selected_band

            # 🚨 Aquí es donde nos aseguramos de que la contraseña se guarde correctamente
            user.set_password(form.cleaned_data["password1"])  # Hashear la contraseña
            user.save()

            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect("user_dashboard")
        else:
            print(form.errors)  # Para ver errores en la terminal

    else:
        form = CustomUserCreationForm()

    return render(request, "rehearsals/register.html", {"form": form})



@login_required
def song_list(request):
    songs = Song.objects.filter(band=request.user.band)
    return render(request, 'rehearsals/song_list.html', {'songs': songs})

@login_required
def create_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.band = request.user.band
            song.save()
            messages.success(request, "Canción agregada.")
            return redirect('song_list')
    else:
        form = SongForm()
    return render(request, 'rehearsals/create_song.html', {'form': form})

@login_required
def create_rehearsal(request):
    if request.method == 'POST':
        form = RehearsalForm(request.POST)
        if form.is_valid():
            rehearsal = form.save(commit=False)
            rehearsal.band = request.user.band
            rehearsal.save()
            rehearsal.songs.set(request.POST.getlist('songs'))
            messages.success(request, "Ensayo agendado.")
            return redirect('rehearsal_list')
    else:
        form = RehearsalForm()
    songs = Song.objects.filter(band=request.user.band)
    return render(request, 'rehearsals/create_rehearsal.html', {'form': form, 'songs': songs})

@login_required
def rehearsal_list(request):
    rehearsals = Rehearsal.objects.filter(band=request.user.band)
    return render(request, 'rehearsals/rehearsal_list.html', {'rehearsals': rehearsals})

@login_required
def rehearsal_detail(request, rehearsal_id):
    rehearsal = get_object_or_404(Rehearsal, id=rehearsal_id)
    return render(request, "rehearsals/rehearsal_detail.html", {"rehearsal": rehearsal})

@login_required
def user_dashboard(request):
    rehearsals = Rehearsal.objects.filter(band=request.user.band)
    return render(request, "rehearsals/user_dashboard.html", {"rehearsals": rehearsals})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Rehearsal

def select_date(request, rehearsal_id):
    rehearsal = get_object_or_404(Rehearsal, id=rehearsal_id)

    if request.method == "POST":
        selected_date = request.POST.get("selected_date")
        selected_time = request.POST.get("selected_time")

        if selected_date and selected_time:
            rehearsal.final_date = selected_date
            rehearsal.final_time = selected_time
            rehearsal.save()
            messages.success(request, f"Fecha y hora confirmadas: {selected_date} a las {selected_time}")
            return redirect("rehearsal_detail", rehearsal_id=rehearsal.id)
        else:
            messages.error(request, "Debes seleccionar una fecha y hora.")

    return render(request, "rehearsals/select_date.html", {"rehearsal": rehearsal})


from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("user_dashboard")
        else:
            messages.error(request, "⚠️ Usuario o contraseña incorrectos. Inténtalo nuevamente.")

    return render(request, "rehearsals/login.html")


@login_required
def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    return render(request, "rehearsals/song_detail.html", {"song": song})


from django.shortcuts import render

def ventajas(request):
    return render(request, 'rehearsals/ventajas.html')

def acerca_de(request):
    return render(request, 'rehearsals/acerca_de.html')
