from django import forms
from .models import Post
from accounts.models import ArtistProfile, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'media', 'thumbnail', 'category', 'price']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Title of your work (Song, Dance performance, Painting, Book, Poem, etc.)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'rows': 4,
                'placeholder': 'Describe your work, lyrics, inspiration, tools, or performance details...'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Price in ₹ (Optional)'
            }),
            'media': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'accept': 'image/*,video/*,audio/*,.pdf'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'accept': 'image/*'
            }),
        }

    def clean_media(self):
        media = self.cleaned_data.get('media')
        if media and hasattr(media, 'size'):
            max_size = 40 * 1024 * 1024  # 40 MB
            if media.size > max_size:
                size_mb = round(media.size / (1024 * 1024), 1)
                raise forms.ValidationError(
                    f"File size ({size_mb} MB) exceeds the 40 MB limit. Please upload a compressed MP4 video, audio, or document file."
                )
        return media

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if thumbnail and hasattr(thumbnail, 'size'):
            max_size = 10 * 1024 * 1024  # 10 MB
            if thumbnail.size > max_size:
                size_mb = round(thumbnail.size / (1024 * 1024), 1)
                raise forms.ValidationError(
                    f"Cover image size ({size_mb} MB) exceeds the 10 MB limit."
                )
        return thumbnail


class ArtistProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = ArtistProfile
        fields = ['artist_type', 'bio', 'location', 'experience_years', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500'}),
            'artist_type': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500'}),
            'experience_years': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500'}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500'}),
        }
