from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import views as auth_views
from .views import select_date, user_dashboard, register_user


urlpatterns = [
    path('', views.home, name='home'),
    path('rehearsals/', views.rehearsal_list, name='rehearsal_list'),
    path('rehearsals/new/', views.create_rehearsal, name='create_rehearsal'),
    path('songs/new/', views.create_song, name='create_song'),
    path('login/', LoginView.as_view(template_name='rehearsals/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('rehearsals/<int:rehearsal_id>/', views.rehearsal_detail, name='rehearsal_detail'),
    path('rehearsals/new/', views.create_rehearsal, name='create_rehearsal'),
    path('rehearsals/<int:rehearsal_id>/select_date/', views.select_date, name='select_date'),
    path('songs/<int:pk>/', views.song_detail, name='song_detail'),
    path('songs/', views.song_list, name='song_list'),
    path('<int:rehearsal_id>/select_date/', select_date, name="select_date"),
    path('dashboard/', user_dashboard, name="user_dashboard"),
    path('register/', register_user, name='register'),  # Nueva ruta para el registro

]