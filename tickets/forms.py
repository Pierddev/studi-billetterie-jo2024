from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Email valide requis.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widget = {
            'username': forms.TextInput,
            'email': forms.EmailField,
            'password1': forms.PasswordInput,
            'password2': forms.PasswordInput
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=("username"),
        widget=forms.TextInput,
    )
    password = forms.CharField(
        label=("password"),
        strip=False,
        widget=forms.PasswordInput,
    )
