from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CreatorRequiredMixin, UserRequiredMixin
from .models import Content, Subscription


class IndexView(ListView):
    model = Content
    fields = '__all__'
    template_name = 'profile.html'

    def get_queryset(self):
        return Content.objects.all()

class ProfileView(ListView):
    model = Content
    fields = '__all__'
    template_name = 'index.html'

    def get_queryset(self):
        return Content.objects.all()

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
    # Проверка прав доступа (аналогичная проверка)
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