from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'gender', 'password1', 'password2']
