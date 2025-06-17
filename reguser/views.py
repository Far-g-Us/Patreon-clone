from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout  as auth_logout
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from home.models import CustomUser, Content
from .forms import UserRegisterForm, ProfileForm


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
            login(request, user)
            messages.success(request, f'Аккаунт успешно создан! Добро пожаловать, {user.username}!')
            return redirect('profile')
    else:
        form = UserRegisterForm()

    return render(request, 'registration.html', {'form': form})


@require_http_methods(["GET", "POST"])
def custom_logout(request):
    if request.method == "POST":
        auth_logout(request)
        messages.success(request, "Вы успешно вышли из системы")
        return redirect('home')
    else:
        # Для GET-запросов показываем страницу подтверждения
        return render(request, 'logout_confirm.html')


# def creator_profile(request, user_id):
#     creator = get_object_or_404(
#         CustomUser,
#         id=user_id,
#         role='creator'
#     )
#     # Проверяем, является ли пользователь создателем
#     # if not creator.is_creator:
#     #     raise Http404("Страница не найдена")
#
#     contents = Content.objects.filter(creator=creator).prefetch_related('tags')
#
#     return render(request, 'creator_profile.html', {
#         'creator': creator,
#         'contents': contents
#     })
#
# @login_required
# def user_profile(request, user_id):
#     profile_user = request.user
#
#     # Для обычных пользователей показываем подписки
#     subscriptions = None
#     if profile_user.role == 'user':
#         subscriptions = profile_user.subscriptions.filter(is_active=True)
#
#     # Для создателей показываем контент
#     contents = None
#     if profile_user.role == 'creator':
#         contents = Content.objects.filter(creator=profile_user)
#
#     return render(request, 'user_profile.html', {
#         'profile_user': profile_user,
#         'subscriptions': subscriptions,
#         'contents': contents
#     })


@login_required
def profile(request, user_id):
    """Единый профиль для всех пользователей"""
    profile_user = get_object_or_404(CustomUser, id=user_id)

    # Для создателей добавляем контент
    contents = None
    if profile_user.role == 'creator':
        contents = Content.objects.filter(creator=profile_user)

    # Для обычных пользователей добавляем подписки
    subscriptions = None
    if request.user.is_authenticated and request.user.id == profile_user.id and profile_user.role == 'user':
        if hasattr(profile_user, 'subscriptions'):
            subscriptions = profile_user.subscriptions.filter(is_active=True)

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'contents': contents,
        'subscriptions': subscriptions
    })


@login_required
def profile_update(request):
    """Обновление профиля для всех пользователей"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Используем GET-параметр для передачи сообщения об успехе
            return redirect('{}?success=1'.format(reverse('profile_update')))
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile_update.html', {
        'form': form,
        'success': request.GET.get('success')
    })

# @login_required
# def creator_profile_update(request, user_id):
#     if request.user.id != user_id or not request.user.is_creator:
#         raise PermissionDenied
#
#     # Проверяем, является ли пользователь создателем
#     if not request.user.is_creator:
#         messages.warning(request, 'Эта страница доступна только создателям контента')
#         return redirect('home')
#
#     if request.method == 'POST':
#         form = CreatorProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Профиль успешно обновлен!')
#             return redirect('profile_update')
#     else:
#         form = CreatorProfileForm(instance=request.user)
#
#     return redirect('creator_profile', user_id=request.user.id)

# @login_required
# def user_settings(request):
#     if request.method == 'POST':
#         form = UserSettingsForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Настройки сохранены!')
#             return redirect('user_settings')
#     else:
#         form = UserSettingsForm(instance=request.user)
#
#     return render(request, 'settings.html', {'form': form})


# def content_list(request):
#     content_list = Content.objects.filter(is_public=True).order_by('-created_at')
#     paginator = Paginator(content_list, 10)  # 10 элементов на страницу
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'list.html', {'page_obj': page_obj})