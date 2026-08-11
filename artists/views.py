from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Avg, Sum, Count
from .models import Post, ArtistType
from .forms import PostForm, ArtistProfileForm
from accounts.models import ArtistProfile, User
from interactions.models import Like, Review, CommissionRequest, Payment


def get_artist_profile(user):
    """Helper function to enforce artist role and return ArtistProfile."""
    if not user.is_authenticated or not user.is_artist():
        raise PermissionDenied("Only registered artists can access this section.")
    profile, created = ArtistProfile.objects.get_or_create(user=user)
    return profile


@login_required
def artist_dashboard_view(request):
    profile = get_artist_profile(request.user)

    total_posts = profile.posts.count()
    total_likes = Like.objects.filter(post__artist=profile).count()

    avg_rating_val = profile.reviews.aggregate(avg=Avg('rating'))['avg']
    avg_rating = round(avg_rating_val, 1) if avg_rating_val else 'N/A'

    pending_requests_count = profile.received_requests.filter(status=CommissionRequest.Status.PENDING).count()
    upcoming_work_count = profile.received_requests.filter(status=CommissionRequest.Status.ACCEPTED).count()
    in_progress_count = profile.received_requests.filter(status=CommissionRequest.Status.IN_PROGRESS).count()
    completed_work_count = profile.received_requests.filter(status=CommissionRequest.Status.COMPLETED).count()

    total_earnings = profile.payments.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'profile': profile,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'avg_rating': avg_rating,
        'pending_requests_count': pending_requests_count,
        'upcoming_work_count': upcoming_work_count,
        'in_progress_count': in_progress_count,
        'completed_work_count': completed_work_count,
        'total_earnings': total_earnings,
    }
    return render(request, 'artists/dashboard.html', context)


@login_required
def artist_profile_edit_view(request):
    profile = get_artist_profile(request.user)

    if request.method == 'POST':
        form = ArtistProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.phone_number = form.cleaned_data.get('phone_number', '')
            request.user.save()

            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('artist_dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ArtistProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        })

    return render(request, 'artists/profile_edit.html', {'form': form, 'profile': profile})


@login_required
def artist_posts_list_view(request):
    profile = get_artist_profile(request.user)
    posts = profile.posts.annotate(likes_count=Count('likes')).all()
    return render(request, 'artists/posts_list.html', {'profile': profile, 'posts': posts})


@login_required
def artist_post_create_view(request):
    profile = get_artist_profile(request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.artist = profile
            post.save()
            messages.success(request, "Portfolio post created successfully!")
            return redirect('artist_posts_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PostForm()

    return render(request, 'artists/post_form.html', {'form': form, 'title': 'Create Portfolio Post'})


@login_required
def artist_post_edit_view(request, pk):
    profile = get_artist_profile(request.user)
    post = get_object_or_404(Post, pk=pk)

    if post.artist != profile:
        raise PermissionDenied("You do not have permission to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Portfolio post updated successfully!")
            return redirect('artist_posts_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PostForm(instance=post)

    return render(request, 'artists/post_form.html', {'form': form, 'title': 'Edit Portfolio Post', 'post': post})


@login_required
def artist_post_delete_view(request, pk):
    profile = get_artist_profile(request.user)
    post = get_object_or_404(Post, pk=pk)

    if post.artist != profile:
        raise PermissionDenied("You do not have permission to delete this post.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Portfolio post deleted.")
        return redirect('artist_posts_list')

    return render(request, 'artists/post_confirm_delete.html', {'post': post})


def public_artist_detail_view(request, artist_id):
    """Public profile view of an artist showing rating summary, reviews, portfolio posts with likes, and CTA buttons."""
    artist_profile = get_object_or_404(ArtistProfile, id=artist_id)
    posts = artist_profile.posts.annotate(likes_count=Count('likes')).all()
    reviews = artist_profile.reviews.select_related('client__user').all()

    avg_rating_val = reviews.aggregate(avg=Avg('rating'))['avg']
    avg_rating = round(avg_rating_val, 1) if avg_rating_val else None
    reviews_count = reviews.count()

    # Track which posts the logged in user has liked
    user_liked_post_ids = []
    if request.user.is_authenticated:
        user_liked_post_ids = list(
            Like.objects.filter(user=request.user, post__artist=artist_profile).values_list('post_id', flat=True)
        )

    context = {
        'artist': artist_profile,
        'posts': posts,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'reviews_count': reviews_count,
        'user_liked_post_ids': user_liked_post_ids,
    }
    return render(request, 'artists/public_profile.html', context)
