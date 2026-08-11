from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:artist_id>/', views.create_commission_request_view, name='create_commission_request'),
    path('client/requests/', views.client_requests_list_view, name='client_requests_list'),
    path('artist/requests/', views.artist_requests_list_view, name='artist_requests_list'),
    path('request/<int:request_id>/status/', views.update_request_status_view, name='update_request_status'),
    path('like/<int:post_id>/', views.toggle_like_post_view, name='toggle_like_post'),
    path('review/<int:request_id>/', views.create_review_view, name='create_review'),
    path('artist/<int:artist_id>/review/', views.create_direct_artist_review_view, name='create_direct_artist_review'),
]
