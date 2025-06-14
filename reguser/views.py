from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, CreatorProfileForm


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Используем стандартную форму аутентификации
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {
        'form': form,
        'next': request.GET.get('next', '')
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Если пользователь регистрируется как создатель
            if user.is_creator():
                profile_form = CreatorProfileForm(request.POST, request.FILES, instance=user)
                if profile_form.is_valid():
                    profile_form.save()

            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'registration.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('home')


@login_required
def creator_profile_update(request):
    # Проверяем, является ли пользователь создателем
    if not request.user.is_creator():
        messages.warning(request, 'Эта страница доступна только создателям контента')
        return redirect('home')

    if request.method == 'POST':
        form = CreatorProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('creator_profile')
    else:
        form = CreatorProfileForm(instance=request.user)

    return render(request, 'profile_update.html', {'form': form})