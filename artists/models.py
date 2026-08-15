import os
from django.db import models


class ArtistType(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g. Photographer, Painter, Musician")
    description = models.TextField(blank=True, help_text="Optional description of this category")

    class Meta:
        ordering = ['name']
        verbose_name = 'Artist Type'
        verbose_name_plural = 'Artist Types'

    def __str__(self):
        return self.name


class Post(models.Model):
    artist = models.ForeignKey(
        'accounts.ArtistProfile',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media = models.FileField(
        upload_to='portfolio_posts/',
        max_length=500,
        help_text="Upload image, video (MP4/WebM), audio (MP3/WAV), or PDF document"
    )
    thumbnail = models.ImageField(
        upload_to='portfolio_thumbnails/',
        max_length=500,
        blank=True,
        null=True,
        help_text="Optional cover/thumbnail image for video, audio, or PDF document"
    )
    category = models.ForeignKey(
        ArtistType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional artwork/service price in ₹"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.artist.user.username}"

    @property
    def file_extension(self):
        if not self.media or not self.media.name:
            return ''
        name_lower = self.media.name.lower()
        if '.avif' in name_lower:
            return '.avif'
        if '.png' in name_lower:
            return '.png'
        if '.jpg' in name_lower or '.jpeg' in name_lower:
            return '.jpg'
        if '.gif' in name_lower:
            return '.gif'
        if '.webp' in name_lower:
            return '.webp'
        if '.pdf' in name_lower:
            return '.pdf'
        if '.mp3' in name_lower:
            return '.mp3'
        if '.wav' in name_lower:
            return '.wav'
        if '.mp4' in name_lower:
            return '.mp4'
        if '.webm' in name_lower:
            return '.webm'
        return os.path.splitext(self.media.name)[1].lower()

    @property
    def is_image(self):
        return self.file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif']

    @property
    def is_video(self):
        return self.file_extension in ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv']

    @property
    def is_audio(self):
        return self.file_extension in ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg']

    @property
    def is_pdf(self):
        return self.file_extension == '.pdf'

    @property
    def media_url(self):
        """
        Returns the clean, correct absolute media URL for images, videos, audio, and PDFs.
        Corrects any mismatched Cloudinary upload endpoints dynamically.
        """
        if not self.media:
            return ''
        url_str = self.media.url
        if self.is_image:
            if url_str.endswith('.mp4'):
                url_str = url_str[:-4]
            if '/video/upload/' in url_str:
                url_str = url_str.replace('/video/upload/', '/image/upload/')
            elif '/raw/upload/' in url_str:
                url_str = url_str.replace('/raw/upload/', '/image/upload/')
        elif self.is_pdf:
            if url_str.endswith('.mp4'):
                url_str = url_str[:-4]
            if '/image/upload/' in url_str:
                url_str = url_str.replace('/image/upload/', '/raw/upload/')
            elif '/video/upload/' in url_str:
                url_str = url_str.replace('/video/upload/', '/raw/upload/')
        elif self.is_video or self.is_audio:
            if '/image/upload/' in url_str:
                url_str = url_str.replace('/image/upload/', '/video/upload/')
        return url_str
