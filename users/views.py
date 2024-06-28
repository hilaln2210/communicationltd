from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm, CustomerForm, SetPasswordForm, ForgotPasswordForm
from .models import User, Customer
import hashlib
import os

from django.utils.html import escape

@login_required
def system_screen(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            # Escape the customer name to prevent XSS attacks
            safe_message = escape(f'לקוח חדש {customer.name} נוסף בהצלחה!')
            messages.success(request, safe_message)
            return redirect('system_screen')
    else:
        form = CustomerForm()

    customers = Customer.objects.filter(user=request.user)
    return render(request, 'users/system_screen.html', {'form': form, 'customers': customers})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'נרשמת בהצלחה!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'התחברת בהצלחה!')
                return redirect('home')
            else:
                messages.error(request, 'שם משתמש או סיסמה לא נכונים.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'התנתקת בהצלחה!')
    return redirect('home')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'הסיסמה שלך שונתה בהצלחה!')
            return redirect('home')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = hashlib.sha256(os.urandom(60)).hexdigest()
                user.password_reset_token = token
                user.save()

                reset_link = request.build_absolute_uri(reverse('reset_password', args=[token]))
                send_mail(
                    'איפוס סיסמה',
                    f'לחץ כאן לאיפוס הסיסמה: {reset_link}',
                    'noreply@example.com',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'הוראות לאיפוס הסיסמה נשלחו למייל שלך.')
                return redirect('password_reset_done')
            else:
                messages.error(request, 'לא נמצא משתמש עם כתובת המייל הזו.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'users/forgot_password.html', {'form': form})

def reset_password(request, token):
    user = User.objects.filter(password_reset_token=token).first()
    if user is None:
        messages.error(request, 'קישור לא תקין או פג תוקף.')
        return redirect('forgot_password')

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            user.password_reset_token = None
            user.save()
            messages.success(request, 'הסיסמה שלך אופסה בהצלחה. אתה יכול להתחבר עכשיו.')
            return redirect('login')
    else:
        form = SetPasswordForm(user)
    return render(request, 'users/reset_password.html', {'form': form})

def password_reset_done(request):
    return render(request, 'users/password_reset_done.html')

@login_required
def home(request):
    return render(request, 'home.html')
