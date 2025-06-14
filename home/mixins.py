from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class CreatorRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки, что пользователь является создателем контента"""

    def dispatch(self, request, *args, **kwargs):
        # Проверяем авторизацию через LoginRequiredMixin
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Проверяем, является ли пользователь создателем
        if not hasattr(request.user, 'is_creator') or not request.user.is_creator():
            raise PermissionDenied("Доступ только для создателей контента")

        return super().dispatch(request, *args, **kwargs)


class UserRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки, что пользователь является обычным пользователем"""

    def dispatch(self, request, *args, **kwargs):
        # Проверяем авторизацию
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Проверяем, что пользователь НЕ создатель
        if hasattr(request.user, 'is_creator') and request.user.is_creator():
            raise PermissionDenied("Доступ только для подписчиков")

        return super().dispatch(request, *args, **kwargs)