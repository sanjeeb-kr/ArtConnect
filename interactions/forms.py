from django import forms
from .models import CommissionRequest, Review


class CommissionRequestForm(forms.ModelForm):
    class Meta:
        model = CommissionRequest
        fields = ['title', 'event_date', 'location', 'budget', 'details']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'e.g. Wedding Photography, Portrait Painting'
            }),
            'event_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Event / Project Location'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Budget in ₹'
            }),
            'details': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Describe what you need, timelines, style preferences, etc.'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(5, 0, -1)],
                attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500'}
            ),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Share your experience working with this artist...'
            }),
        }
