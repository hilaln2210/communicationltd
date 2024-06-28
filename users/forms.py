from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Customer
import re
from django.conf import settings

User = get_user_model()

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='כתובת אימייל')

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < settings.PASSWORD_CONFIG['MIN_LENGTH']:
            raise ValidationError(f"הסיסמה חייבת להכיל לפחות {settings.PASSWORD_CONFIG['MIN_LENGTH']} תווים.")
        if not re.search(r'\d', password):
            raise ValidationError("הסיסמה חייבת להכיל לפחות ספרה אחת.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("הסיסמה חייבת להכיל לפחות אות גדולה אחת.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("הסיסמה חייבת להכיל לפחות אות קטנה אחת.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise ValidationError("הסיסמה חייבת להכיל לפחות תו מיוחד אחד.")
        return password

class UserLoginForm(forms.Form):
    username = forms.CharField(label='שם משתמש')
    password = forms.CharField(label='סיסמה', widget=forms.PasswordInput)

class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if len(password) < settings.PASSWORD_CONFIG['MIN_LENGTH']:
            raise ValidationError(f"הסיסמה חייבת להכיל לפחות {settings.PASSWORD_CONFIG['MIN_LENGTH']} תווים.")
        if not re.search(r'\d', password):
            raise ValidationError("הסיסמה חייבת להכיל לפחות ספרה אחת.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("הסיסמה חייבת להכיל לפחות אות גדולה אחת.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("הסיסמה חייבת להכיל לפחות אות קטנה אחת.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise ValidationError("הסיסמה חייבת להכיל לפחות תו מיוחד אחד.")
        return password

class CustomerForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Customer
        fields = ['name', 'phone']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
