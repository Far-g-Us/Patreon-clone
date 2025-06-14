from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
]