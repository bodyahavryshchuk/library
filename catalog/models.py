from django.db import models
from datetime import date
from django.contrib.auth.models import User

from django.urls import reverse  # To generate URLS by reversing URL patterns


class Genre(models.Model):
    """Модель жанру книги"""
    name = models.CharField(
        max_length=200,
        help_text="Введіть жанр книги", verbose_name="Жанр"
        )

    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Language(models.Model):
    """Модель мови книги"""
    name = models.CharField(max_length=200,
                            help_text="Введіть мову, на якій написана книга", verbose_name="Мова")

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель книги"""
    title = models.CharField(max_length=200, verbose_name="Назва")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    summary = models.TextField(max_length=1000, help_text="Введіть короткий опис книги", verbose_name="Опис")
    genre = models.ManyToManyField(Genre, help_text="Виберіть жанр книги", verbose_name="Жанр")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, verbose_name="Мова")
    book_file = models.FileField(upload_to='books_files/', verbose_name="Файл книги")

    def delete(self, *args, **kwargs):
        self.book_file.delete(save=False)
        super().delete(*args, **kwargs)

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Жанр'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class Author(models.Model):
    """Модель авора книги"""
    first_name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    date_of_birth = models.DateField('Дата народження',null=True, blank=True)
    date_of_death = models.DateField('Дата смерті', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)
