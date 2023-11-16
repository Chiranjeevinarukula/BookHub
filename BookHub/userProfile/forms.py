from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class signUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2','email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_pic','favorite_genres']
    
class UserForm(forms.ModelForm):
   class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']