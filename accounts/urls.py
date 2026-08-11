from django.urls import path
from . import views

urlpatterns = [
    path('register/artist/', views.register_artist_view, name='register_artist'),
    path('register/client/', views.register_client_view, name='register_client'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
