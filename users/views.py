from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import UserProfile


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login_required(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('shop:product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вход выполнен успешно!')
            return redirect('shop:product_list')
        else:
            messages.error(request, 'Неправильный логин или пароль! Попробуйте еще раз!')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('shop:product_list')


@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен успешно')
            return redirect('users:profile')
        else:
            messages.error(request, 'Исправьте ошибки в форме!')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/profile.html', {'form': form})

