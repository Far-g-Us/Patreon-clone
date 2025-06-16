from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset_form.html',
             subject_template_name='password_reset_subject.txt'
         ),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('settings/', views.user_settings, name='user_settings'),

    # Для обычного пользователя
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),

    # Для создателей
    path('creator/<int:user_id>/', views.creator_profile, name='creator_profile'),
]