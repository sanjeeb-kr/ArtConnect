from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ARTIST = 'ARTIST', 'Artist'
        CLIENT = 'CLIENT', 'Client'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
        help_text="User role: ARTIST or CLIENT"
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def is_artist(self):
        return self.role == self.Role.ARTIST

    def is_client(self):
        return self.role == self.Role.CLIENT

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class ArtistProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='artist_profile'
    )
    artist_type = models.ForeignKey(
        'artists.ArtistType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='artists'
    )
    bio = models.TextField(blank=True, help_text="Short background and statement")
    location = models.CharField(max_length=100, blank=True, help_text="City / State / Country")
    experience_years = models.PositiveIntegerField(default=0, help_text="Years of creative experience")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        type_str = self.artist_type.name if self.artist_type else 'Artist'
        return f"{self.user.get_full_name() or self.user.username} - {type_str}"


class ClientProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    location = models.CharField(max_length=100, blank=True, help_text="City / State / Country")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} (Client)"
