from django.urls import path
from . import views
from .views import (
    UnifiedPasswordResetView,
    UnifiedPasswordResetDoneView,
    UnifiedPasswordResetConfirmView,
    UnifiedPasswordResetCompleteView
)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    path('password-reset/', UnifiedPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', UnifiedPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UnifiedPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', UnifiedPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Для обычного пользователя
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    # Для создателей
    # path('creator/<int:user_id>/', views.creator_profile, name='creator_profile'),
]