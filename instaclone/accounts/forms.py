from django import forms
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.ModelForm):

class SignupForm(UserCreationForm):