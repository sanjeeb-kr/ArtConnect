from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User, ArtistProfile, ClientProfile
from artists.models import Post


class CommissionRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    client = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )
    artist = models.ForeignKey(
        ArtistProfile,
        on_delete=models.CASCADE,
        related_name='received_requests'
    )
    title = models.CharField(max_length=200, help_text="e.g. Wedding Photography, Custom Portrait")
    event_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=150, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, help_text="Budget in ₹")
    details = models.TextField(help_text="Provide specific project details, requirements, or location notes")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request: '{self.title}' ({self.client.user.username} -> {self.artist.user.username}) - {self.get_status_display()}"


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_like')
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


class Review(models.Model):
    client = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name='reviews_written'
    )
    artist = models.ForeignKey(
        ArtistProfile,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    request = models.OneToOneField(
        CommissionRequest,
        on_delete=models.CASCADE,
        related_name='review',
        null=True,
        blank=True
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating between 1 and 5"
    )
    comment = models.TextField(help_text="Write your review about working with this artist")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review ({self.rating}/5) by {self.client.user.username} for {self.artist.user.username}"


class Payment(models.Model):
    request = models.OneToOneField(
        CommissionRequest,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    artist = models.ForeignKey(
        ArtistProfile,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment ₹{self.amount} for '{self.request.title}' ({self.artist.user.username})"
