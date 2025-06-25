from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home, song_list, create_song, create_rehearsal, rehearsal_list,
    rehearsal_detail, select_date, user_dashboard, register_user, song_detail, ventajas
)
from . import views


urlpatterns = [
    path("", home, name="home"),
    path("songs/", song_list, name="song_list"),
    path("songs/new/", create_song, name="create_song"),
    path("songs/<int:song_id>/", song_detail, name="song_detail"),

    path("rehearsals/", rehearsal_list, name="rehearsal_list"),
    path("rehearsals/new/", create_rehearsal, name="create_rehearsal"),
    path("rehearsals/<int:rehearsal_id>/", rehearsal_detail, name="rehearsal_detail"),
    path("rehearsals/<int:rehearsal_id>/select-date/", select_date, name="select_date"),

    path("dashboard/", user_dashboard, name="user_dashboard"),
    path("register/", register_user, name="register"),

    path("login/", auth_views.LoginView.as_view(
        template_name="rehearsals/login.html",
        redirect_authenticated_user=True
    ), name="login"),
    
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Nueva ruta para la página de ventajas
    path("ventajas/", ventajas, name="ventajas"),

    path('acerca-de/', views.acerca_de, name='acerca_de'),



]
