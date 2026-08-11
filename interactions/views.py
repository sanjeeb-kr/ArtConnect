from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from accounts.models import ArtistProfile, ClientProfile
from artists.models import Post
from .models import CommissionRequest, Like, Review, Payment
from .forms import CommissionRequestForm, ReviewForm


@login_required
def create_commission_request_view(request, artist_id):
    if not request.user.is_client():
        messages.error(request, "Only clients can send commission requests.")
        return redirect('public_artist_detail', artist_id=artist_id)

    artist = get_object_or_404(ArtistProfile, id=artist_id)
    client_profile = request.user.client_profile

    if request.method == 'POST':
        form = CommissionRequestForm(request.POST)
        if form.is_valid():
            comm_request = form.save(commit=False)
            comm_request.client = client_profile
            comm_request.artist = artist
            comm_request.status = CommissionRequest.Status.PENDING
            comm_request.save()
            messages.success(request, f"Your request for '{comm_request.title}' has been sent to {artist.user.get_full_name() or artist.user.username}!")
            return redirect('client_requests_list')
        else:
            messages.error(request, "Please correct the errors in your request.")
    else:
        form = CommissionRequestForm()

    return render(request, 'interactions/request_form.html', {
        'form': form,
        'artist': artist,
    })


@login_required
def client_requests_list_view(request):
    if not request.user.is_client():
        raise PermissionDenied("Only clients can access this view.")

    client_profile = request.user.client_profile
    requests_list = client_profile.sent_requests.select_related('artist__user', 'review').all()
    return render(request, 'interactions/client_requests.html', {'requests_list': requests_list})


@login_required
def artist_requests_list_view(request):
    if not request.user.is_artist():
        raise PermissionDenied("Only artists can access this view.")

    artist_profile = request.user.artist_profile
    status_filter = request.GET.get('status', '').strip().upper()

    requests_list = artist_profile.received_requests.select_related('client__user').all()

    if status_filter in dict(CommissionRequest.Status.choices):
        requests_list = requests_list.filter(status=status_filter)

    context = {
        'artist_profile': artist_profile,
        'requests_list': requests_list,
        'selected_status': status_filter,
    }
    return render(request, 'interactions/artist_requests.html', context)


@login_required
def update_request_status_view(request, request_id):
    if not request.user.is_artist():
        raise PermissionDenied("Only artists can update request status.")

    artist_profile = request.user.artist_profile
    comm_request = get_object_or_404(CommissionRequest, id=request_id)

    if comm_request.artist != artist_profile:
        raise PermissionDenied("You can only manage requests sent to you.")

    if request.method == 'POST':
        new_status = request.POST.get('status', '').strip().upper()
        if new_status in dict(CommissionRequest.Status.choices):
            comm_request.status = new_status
            comm_request.save()

            # Automatic Payment Record Generation on Completion
            if new_status == CommissionRequest.Status.COMPLETED:
                Payment.objects.get_or_create(
                    request=comm_request,
                    artist=artist_profile,
                    defaults={'amount': comm_request.budget}
                )
                messages.success(request, f"Work marked as COMPLETED! Earnings of ₹{comm_request.budget} logged.")
            else:
                messages.success(request, f"Request status updated to {comm_request.get_status_display()}.")
        else:
            messages.error(request, "Invalid status choice.")

    return redirect('artist_requests_list')


@login_required
def toggle_like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_obj = Like.objects.filter(user=request.user, post=post).first()

    if like_obj:
        like_obj.delete()
        messages.info(request, f"Unliked '{post.title}'.")
    else:
        Like.objects.create(user=request.user, post=post)
        messages.success(request, f"Liked '{post.title}'!")

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('public_artist_detail', artist_id=post.artist.id)


@login_required
def create_review_view(request, request_id):
    if not request.user.is_client():
        raise PermissionDenied("Only clients can write reviews.")

    client_profile = request.user.client_profile
    comm_request = get_object_or_404(CommissionRequest, id=request_id)

    if comm_request.client != client_profile:
        raise PermissionDenied("You can only review your own completed requests.")

    if comm_request.status != CommissionRequest.Status.COMPLETED:
        messages.error(request, "You can only review requests that are marked COMPLETED.")
        return redirect('client_requests_list')

    if hasattr(comm_request, 'review'):
        messages.info(request, "You have already submitted a review for this request.")
        return redirect('client_requests_list')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = client_profile
            review.artist = comm_request.artist
            review.request = comm_request
            review.save()
            messages.success(request, f"Thank you for reviewing {comm_request.artist.user.get_full_name() or comm_request.artist.user.username}!")
            return redirect('client_requests_list')
    else:
        form = ReviewForm()

    return render(request, 'interactions/review_form.html', {
        'form': form,
        'comm_request': comm_request,
    })


@login_required
def create_direct_artist_review_view(request, artist_id):
    """Allows a logged-in client to directly rate and review an artist."""
    if not request.user.is_client():
        messages.error(request, "Only registered clients can rate and review artists.")
        return redirect('public_artist_detail', artist_id=artist_id)

    artist_profile = get_object_or_404(ArtistProfile, id=artist_id)
    client_profile = request.user.client_profile

    if artist_profile.user == request.user:
        messages.error(request, "Artists cannot rate or review themselves.")
        return redirect('public_artist_detail', artist_id=artist_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = client_profile
            review.artist = artist_profile
            review.save()
            messages.success(request, f"Thank you for rating {artist_profile.user.get_full_name() or artist_profile.user.username}!")
            return redirect('public_artist_detail', artist_id=artist_id)
    else:
        form = ReviewForm()

    return render(request, 'interactions/review_artist_form.html', {
        'form': form,
        'artist': artist_profile,
    })
