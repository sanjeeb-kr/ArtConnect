from django import forms
from .models import CommissionRequest, Review


class CommissionRequestForm(forms.ModelForm):
    class Meta:
        model = CommissionRequest
        fields = ['title', 'event_date', 'location', 'budget', 'details']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Wedding Photography, Custom Portrait'}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'location': forms.TextInput(attrs={'placeholder': 'Event / Project Location'}),
            'budget': forms.NumberInput(attrs={'placeholder': 'Budget in ₹'}),
            'details': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe what you need, timelines, style preferences, etc.'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(5, 0, -1)]
            ),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience working with this artist...'}),
        }
