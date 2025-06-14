from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, CreatorProfileForm


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


def creator_profile_update(request):
    if not request.user.is_creator():
        return redirect('home')

    if request.method == 'POST':
        form = CreatorProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('creator_dashboard')
    else:
        form = CreatorProfileForm(instance=request.user)

    return render(request, 'profile_update.html', {'form': form})