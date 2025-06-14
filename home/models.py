from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название', db_index=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    #password = models.CharField(max_length=100, blank=True)   # Опционально: защита паролем
    image = models.ImageField(verbose_name='Изображение', upload_to='article/%Y/%m', blank=True)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.title, self.file.name

    class Meta:
        verbose_name = '#'
        verbose_name_plural = '#'