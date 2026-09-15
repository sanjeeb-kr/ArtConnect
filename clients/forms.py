from django import forms
from accounts.models import ClientProfile
from accounts.validators import validate_mobile_number


class ClientProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False, validators=[validate_mobile_number])

    class Meta:
        model = ClientProfile
        fields = ['location', 'profile_picture']
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
        }
