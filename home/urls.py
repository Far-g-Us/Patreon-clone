from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.subscription_list, name='subscription_list'),
]