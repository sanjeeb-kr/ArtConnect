from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, ArtistProfile, ClientProfile
from artists.models import ArtistType


class ArtistRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)

    artist_type = forms.ModelChoiceField(
        queryset=ArtistType.objects.all(),
        required=True,
        empty_label="Select your primary discipline"
    )
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    location = forms.CharField(max_length=100, required=False)
    experience_years = forms.IntegerField(min_value=0, initial=0, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.ARTIST
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number', '')

        if commit:
            user.save()
            ArtistProfile.objects.create(
                user=user,
                artist_type=self.cleaned_data['artist_type'],
                bio=self.cleaned_data.get('bio', ''),
                location=self.cleaned_data.get('location', ''),
                experience_years=self.cleaned_data.get('experience_years', 0),
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        return user


class ClientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)

    location = forms.CharField(max_length=100, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CLIENT
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number', '')

        if commit:
            user.save()
            ClientProfile.objects.create(
                user=user,
                location=self.cleaned_data.get('location', ''),
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Password'
        })
    )
