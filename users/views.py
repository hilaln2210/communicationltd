from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .forms import UserRegistrationForm, UserLoginForm, CustomerForm, SetPasswordForm, ForgotPasswordForm
from .models import User, Customer, Package, Subscription
import hashlib
import os

from django.utils.html import escape


def home(request):
    context = {}
    if request.user.is_authenticated:
        customers = Customer.objects.filter(user=request.user)
        today = timezone.now().date()
        active_subs = Subscription.objects.filter(
            customer__user=request.user,
            end_date__gte=today
        ).count()
        packages_count = Package.objects.count()
        context = {
            'num_customers': customers.count(),
            'active_subscriptions': active_subs,
            'packages_count': packages_count,
        }
    return render(request, 'home.html', context)


@login_required
def system_screen(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            safe_message = escape(f'לקוח חדש {customer.name} נוסף בהצלחה!')
            messages.success(request, safe_message)
            return redirect('system_screen')
    else:
        form = CustomerForm()

    customers = Customer.objects.filter(user=request.user).prefetch_related('subscription_set__package')
    today = timezone.now().date()
    customers_with_subs = []
    for c in customers:
        active_sub = c.subscription_set.filter(end_date__gte=today).first()
        customers_with_subs.append({
            'customer': c,
            'active_sub': active_sub,
        })

    return render(request, 'users/system_screen.html', {
        'form': form,
        'customers_with_subs': customers_with_subs,
    })


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
    if request.method == 'POST':
        name = customer.name
        customer.delete()
        messages.success(request, f'הלקוח {escape(name)} נמחק בהצלחה.')
    return redirect('system_screen')


@login_required
def packages_view(request):
    packages = Package.objects.all()
    customers = Customer.objects.filter(user=request.user)
    return render(request, 'users/packages.html', {'packages': packages, 'customers': customers})


@login_required
def subscribe_customer(request, customer_pk, package_pk):
    customer = get_object_or_404(Customer, pk=customer_pk, user=request.user)
    package = get_object_or_404(Package, pk=package_pk)

    if request.method == 'POST':
        today = timezone.now().date()
        end_date = today.replace(year=today.year + 1)
        Subscription.objects.create(
            customer=customer,
            package=package,
            start_date=today,
            end_date=end_date,
        )
        messages.success(request, f'הלקוח {escape(customer.name)} נרשם לחבילה {escape(package.name)} בהצלחה!')
        return redirect('system_screen')

    return render(request, 'users/subscribe_confirm.html', {
        'customer': customer,
        'package': package,
    })


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
                user.token_created_at = timezone.now()
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

    # Check token expiry — tokens older than 1 hour are invalid
    if user.token_created_at and timezone.now() - user.token_created_at > timedelta(hours=1):
        user.password_reset_token = None
        user.token_created_at = None
        user.save()
        messages.error(request, 'קישור האיפוס פג תוקף. אנא בקש קישור חדש.')
        return redirect('forgot_password')

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            user.password_reset_token = None
            user.token_created_at = None
            user.save()
            messages.success(request, 'הסיסמה שלך אופסה בהצלחה. אתה יכול להתחבר עכשיו.')
            return redirect('login')
    else:
        form = SetPasswordForm(user)
    return render(request, 'users/reset_password.html', {'form': form})


def password_reset_done(request):
    return render(request, 'users/password_reset_done.html')
