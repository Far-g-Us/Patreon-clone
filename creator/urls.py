from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('<int:user_id>/', ProfileView.as_view(), name='profile'),
]