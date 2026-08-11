from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.client_dashboard_view, name='client_dashboard'),
    path('profile/edit/', views.client_profile_edit_view, name='client_profile_edit'),
    path('artists/', views.artist_discovery_view, name='artist_discovery'),
]
