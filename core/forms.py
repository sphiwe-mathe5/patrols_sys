from django import forms
from .models import Resident

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['surname', 'house_number', 'street_name', 'place_name']
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control'}),
            'place_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

