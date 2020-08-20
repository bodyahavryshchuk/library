from django.contrib import admin

from .models import Author, Genre, Book, Language

admin.site.register(Genre) #Адмін модель жанру
admin.site.register(Language) #Адмін модель мови


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Адмінмодель автора"""
    list_display = ('last_name',
                    'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')


admin.site.register(Book, BookAdmin) #Адмін книги



