from .models import Profile
from django import forms
from .models import Dodo, Update


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
        fields = ("grade", "city", "date_of_birth")
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = ("dodo", "date", "description")
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    dodo = forms.ModelChoiceField(
        queryset=Dodo.objects.filter(alive=True),
        label="Dodo"
    )
