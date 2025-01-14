from datetime import date, datetime, timedelta
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import  Profile, CustomUser
from django import forms

from submit import models



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']  # Removed username


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long.")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The two password fields must match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={

                }
            )
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    phone_number = forms.CharField()

    class Meta:
        model = User
        fields = ['email']


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


