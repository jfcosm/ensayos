from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('songs/', views.song_list, name='song_list'),
    path('rehearsals/', views.rehearsal_list, name='rehearsal_list'),
    path('rehearsals/new/', views.create_rehearsal, name='create_rehearsal'),
    path('songs/new/', views.create_song, name='create_song'),
    path('login/', auth_views.LoginView.as_view(template_name='rehearsals/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('rehearsals/<int:rehearsal_id>/', views.rehearsal_detail, name='rehearsal_detail'),
    path('rehearsals/new/', views.create_rehearsal, name='create_rehearsal'),
    path('rehearsals/<int:rehearsal_id>/select_date/', views.select_date, name='select_date'),

]
