from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import ArtistRegistrationForm, ClientRegistrationForm, UserLoginForm


def register_artist_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ArtistRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to ArtConnect, {user.first_name}! Your artist profile has been created.")
            return redirect('artist_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ArtistRegistrationForm()

    return render(request, 'accounts/register_artist.html', {'form': form})


def register_client_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to ArtConnect, {user.first_name}! Your client profile has been created.")
            return redirect('client_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ClientRegistrationForm()

    return render(request, 'accounts/register_client.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_artist():
            return redirect('artist_dashboard')
        elif request.user.is_client():
            return redirect('client_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            
            # Role-based dashboard redirect
            if user.is_artist():
                return redirect('artist_dashboard')
            elif user.is_client():
                return redirect('client_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
