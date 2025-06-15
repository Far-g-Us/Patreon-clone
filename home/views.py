from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from .mixins import CreatorRequiredMixin, UserRequiredMixin
from .models import Content, Subscription, CustomUser


@cache_page(60 * 15)
def home(request):
    featured_creators = CustomUser.objects.filter(
        is_creator=True
    ).order_by('-date_joined')[:5]

    return render(request, 'index.html', {
        'featured_creators': featured_creators
    })

class ContentDetailView(LoginRequiredMixin, DetailView):
    model = Content

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверка доступа
        user_has_access = (
                self.object.is_public or
                self.request.user.subscriptions.filter(
                    tier=self.object.tier,
                    is_active=True
                ).exists()
        )
        context['user_has_access'] = user_has_access
        return context


# Для скачивания файлов
from django.http import FileResponse


def download_content(request, pk):
    content = get_object_or_404(Content, pk=pk)
    # Проверка прав доступа
    if not content.is_public and not request.user.subscriptions.filter(tier=content.tier).exists():
        raise PermissionDenied("У вас нет доступа к этому файлу")

    return FileResponse(content.file.open(), as_attachment=True)


# Для создателей контента
class ContentCreateView(CreatorRequiredMixin, CreateView):
    model = Content
    fields = ['title', 'file', 'description', 'tier', 'is_public']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


# Для обычных пользователей
class SubscriptionListView(UserRequiredMixin, ListView):
    model = Subscription
    context_object_name = 'subscriptions'

    def get_queryset(self):
        return self.request.user.subscriptions.filter(is_active=True)