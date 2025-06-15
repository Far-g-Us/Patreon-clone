from django.shortcuts import render
from django.views.generic import ListView
from home.models import Content


class ProfileView(ListView):
    model = Content
    fields = '__all__'
    template_name = 'profile.html'

    def get_queryset(self):
        return Content.objects.all()
