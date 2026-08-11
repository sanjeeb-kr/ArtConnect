from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q, Avg, Count
from accounts.models import ArtistProfile, ClientProfile
from artists.models import ArtistType
from .forms import ClientProfileForm


def get_client_profile(user):
    if not user.is_authenticated or not user.is_client():
        raise PermissionDenied("Only clients can access client management features.")
    profile, created = ClientProfile.objects.get_or_create(user=user)
    return profile


@login_required
def client_dashboard_view(request):
    profile = get_client_profile(request.user)

    active_requests_count = profile.sent_requests.filter(status__in=['PENDING', 'ACCEPTED', 'IN_PROGRESS']).count()
    completed_requests_count = profile.sent_requests.filter(status='COMPLETED').count()
    reviews_left_count = profile.reviews_written.count()

    context = {
        'profile': profile,
        'active_requests_count': active_requests_count,
        'completed_requests_count': completed_requests_count,
        'reviews_left_count': reviews_left_count,
    }
    return render(request, 'clients/dashboard.html', context)


@login_required
def client_profile_edit_view(request):
    profile = get_client_profile(request.user)

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.phone_number = form.cleaned_data.get('phone_number', '')
            request.user.save()

            form.save()
            messages.success(request, "Your client profile has been updated.")
            return redirect('client_dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ClientProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        })

    return render(request, 'clients/profile_edit.html', {'form': form, 'profile': profile})


def artist_discovery_view(request):
    """
    Public / Client view to browse and search artists with QuerySet filtering and average ratings.
    """
    artists = ArtistProfile.objects.select_related('user', 'artist_type').annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    )
    artist_types = ArtistType.objects.all()

    # Filter params
    search_query = request.GET.get('q', '').strip()
    selected_type = request.GET.get('artist_type', '').strip()
    selected_location = request.GET.get('location', '').strip()

    if search_query:
        artists = artists.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(bio__icontains=search_query)
        )

    if selected_type and selected_type.isdigit():
        artists = artists.filter(artist_type_id=int(selected_type))

    if selected_location:
        artists = artists.filter(location__icontains=selected_location)

    context = {
        'artists': artists,
        'artist_types': artist_types,
        'search_query': search_query,
        'selected_type': selected_type,
        'selected_location': selected_location,
    }
    return render(request, 'clients/artist_discovery.html', context)
