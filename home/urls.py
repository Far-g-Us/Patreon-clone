from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('subscription/', views.subscription_list, name='subscription_list'),
    path('create/', views.content_create, name='content_create'),
    path('<int:pk>/', views.content_detail, name='content_detail'),
    path('creators/', views.creator_list, name='creator_list'),
]