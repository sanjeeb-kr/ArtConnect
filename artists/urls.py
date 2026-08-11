from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.artist_dashboard_view, name='artist_dashboard'),
    path('profile/edit/', views.artist_profile_edit_view, name='artist_profile_edit'),
    path('posts/', views.artist_posts_list_view, name='artist_posts_list'),
    path('posts/create/', views.artist_post_create_view, name='artist_post_create'),
    path('posts/<int:pk>/edit/', views.artist_post_edit_view, name='artist_post_edit'),
    path('posts/<int:pk>/delete/', views.artist_post_delete_view, name='artist_post_delete'),
    path('<int:artist_id>/', views.public_artist_detail_view, name='public_artist_detail'),
]
