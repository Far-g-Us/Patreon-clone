from django.views.generic import ListView, DetailView
from home.models import Article


class IndexView(ListView):
    model = Article
    fields = '__all__'
    template_name = 'profile.html'

    def get_queryset(self):
        return Article.objects.all()

