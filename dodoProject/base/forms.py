from .models import Profile
from django import forms
from .models import Dodo


class DodoForm(forms.ModelForm):
    class Meta:
        model = Dodo
        fields = ("name", "date_of_birth")
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("length", "full_name")
