from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Band(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre de la banda")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Rehearsal(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="rehearsals", null=True, blank=True)
    date_option_1 = models.DateField(verbose_name="Primera opción de fecha")
    time_option_1 = models.TimeField(verbose_name="Horario primera opción", null=True, blank=True)
    date_option_2 = models.DateField(verbose_name="Segunda opción de fecha", null=True, blank=True)
    time_option_2 = models.TimeField(verbose_name="Horario segunda opción", null=True, blank=True)
    date_option_3 = models.DateField(verbose_name="Tercera opción de fecha", null=True, blank=True)
    time_option_3 = models.TimeField(verbose_name="Horario tercera opción", null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name="Ubicación")
    songs = models.ManyToManyField("Song", verbose_name="Canciones")
    final_date = models.DateField(null=True, blank=True, verbose_name="Fecha definitiva")
    final_time = models.TimeField(null=True, blank=True, verbose_name="Hora definitiva")

    def __str__(self):
        return f"Ensayo en {self.location} - {self.band.name}"

class Song(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="songs", null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name="Título")
    lyrics_and_chords = models.TextField(verbose_name="Letras y Acordes", default='')

    def __str__(self):
        return f"{self.title} ({self.band.name})"


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("El nombre de usuario debe estar definido.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    band = models.ForeignKey('Band', on_delete=models.CASCADE, related_name="members", null=True, blank=True)

    objects = CustomUserManager()  # Importante para la autenticación

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Evita colisión con 'User.groups'
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # Evita colisión con 'User.user_permissions'
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.band.name if self.band else 'Sin banda'})"
