from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import ContentForm
from .mixins import CreatorRequiredMixin, UserRequiredMixin
from .models import Content, Subscription, CustomUser, DownloadHistory
from django.http import FileResponse, Http404


def download_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)

    # Проверка аутентификации
    if not request.user.is_authenticated:
        return redirect('login')

    # Проверка доступа
    if not content.is_public:
        # Проверяем активные подписки пользователя
        if not request.user.subscriptions.filter(tier=content.tier, is_active=True).exists():
            raise PermissionDenied("У вас нет подписки на необходимый уровень")

    # Используем транзакцию для атомарности
    with transaction.atomic():
        # Увеличиваем счетчик скачиваний
        Content.objects.filter(id=content_id).update(
            download_count=F('download_count') + 1
        )

        # Создаем запись в истории скачиваний
        DownloadHistory.objects.create(
            user=request.user,
            content=content
        )

    # Отправляем файл
    try:
        response = FileResponse(content.file.open(), as_attachment=True)
        response['Content-Length'] = content.file_size
        return response
    except FileNotFoundError:
        raise Http404("Файл не найден")


def home(request):
    # Популярные создатели
    featured_creators = CustomUser.objects.filter(role='creator').order_by('-date_joined')[:5]

    # Последние публичные посты
    latest_posts = Content.objects.filter(is_public=True).order_by('-created_at')[:5]

    # Подписки текущего пользователя (только для авторизованных)
    user_subscriptions = None
    user_contents = None

    if request.user.is_authenticated:
        # Для обычных пользователей
        if hasattr(request.user, 'role') and request.user.role == 'user':
            user_subscriptions = Subscription.objects.filter(
                user=request.user,
                is_active=True
            ).select_related('tier')[:5]

        # Для создателей контента
        elif hasattr(request.user, 'role') and request.user.role == 'creator':
            user_contents = Content.objects.filter(
                creator=request.user
            ).order_by('-created_at')[:5]

    return render(request, 'index.html', {
        'featured_creators': featured_creators,
        'latest_posts': latest_posts,
        'user_subscriptions': user_subscriptions,
        'user_contents': user_contents
    })


def content_detail(request, pk):
    content = get_object_or_404(Content, pk=pk)

    # Проверка доступа
    user_has_access = False
    if request.user.is_authenticated:
        if content.is_public or content.creator == request.user:
            user_has_access = True
        elif request.user.role == 'user':
            user_has_access = request.user.subscriptions.filter(
                tier=content.tier,
                is_active=True
            ).exists()

    return render(request, 'content_detail.html', {
        'content': content,
        'user_has_access': user_has_access
    })


@login_required
def content_create(request):
    # Проверяем, что пользователь является создателем
    if not request.user.is_creator:
        messages.error(request, "Только создатели контента могут добавлять посты")
        return redirect('home')

    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, creator=request.user)
        if form.is_valid():
            content = form.save(commit=False)
            content.creator = request.user
            content.save()
            messages.success(request, "Пост успешно создан!")
            return redirect('content_detail', pk=content.pk)
    else:
        form = ContentForm(creator=request.user)

    return render(request, 'content_create.html', {'form': form})


def creator_list(request):
    creators = CustomUser.objects.filter(role='creator')
    return render(request, 'creator_list.html', {'creators': creators})


@login_required
def subscription_list(request):
    if not request.user.role == 'user':
        return redirect('home')

    subscriptions = Subscription.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('tier')

    return render(request, 'subscriptions_list.html', {
        'subscriptions': subscriptions
    })


def about(request):
    return render(request, 'about.html')


# # Для создателей контента
# class ContentCreateView(CreatorRequiredMixin, CreateView):
#     model = Content
#     fields = ['title', 'file', 'description', 'tier', 'is_public']
#
#     def form_valid(self, form):
#         form.instance.creator = self.request.user
#         return super().form_valid(form)
#
#
# # Для обычных пользователей
# class SubscriptionListView(UserRequiredMixin, ListView):
#     model = Subscription
#     context_object_name = 'subscriptions'
#
#     def get_queryset(self):
#         return self.request.user.subscriptions.filter(is_active=True)