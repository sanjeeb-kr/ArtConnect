from django.contrib import admin
from .models import CommissionRequest, Like, Review, Payment


@admin.register(CommissionRequest)
class CommissionRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'artist', 'budget', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'client__user__username', 'artist__user__username', 'location')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('artist', 'client', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('artist__user__username', 'client__user__username', 'comment')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('request', 'artist', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('artist__user__username', 'request__title')
