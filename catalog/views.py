from django.shortcuts import render

# Create your views here.

from .models import Book, Author, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from .forms import BookCreateForm

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

from django.views import generic


def index(request):
    """Головна сторінка"""
    # Кількість книжок
    num_books = Book.objects.all().count()
    # Кількість авторів
    num_authors = Author.objects.count()

    # Кількість відвідувань сторінки
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_authors': num_authors,
                 'num_visits': num_visits},
    )


class BookCreate(PermissionRequiredMixin, CreateView):
    """Створення книги"""
    permission_required = 'catalog.can_mark_returned'

    def get(self, request, *args, **kwargs):
        context = {'form': BookCreateForm()}
        return render(request, 'catalog/book_form.html', context)

    def post(self, request, *args, **kwargs):
        form = BookCreateForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            book.save()
            return HttpResponseRedirect(reverse_lazy('book-detail', args=[book.id]))
        return render(request, 'catalog/book_form.html', {'form': form})


class BookListView(generic.ListView):
    """Список книжок"""
    model = Book
    paginate_by = 6


class BookDetailView(generic.DetailView):
    """Детальна інформація книжки"""
    model = Book


class BookUpdate(PermissionRequiredMixin, UpdateView):
    """Редагування книги"""
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    """Видалення книги"""
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'


class AuthorCreate(PermissionRequiredMixin, CreateView):
    """Створення автора"""
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    """Редагування автора"""
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    """Видалення автора"""
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


class AuthorListView(generic.ListView):
    """Список авторів"""
    model = Author
    paginate_by = 9


class AuthorDetailView(generic.DetailView):
    """Детальна інформація автора"""
    model = Author


class GenreCreate(PermissionRequiredMixin, CreateView):
    """Створення жанру"""
    model = Genre
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class GenreListView(generic.ListView):
    """Список жанрів"""
    model = Genre
    paginate_by = 9


class GenreDetailView(generic.DetailView):
    """Детальна іформація жанру"""
    model = Genre


class Search(generic.ListView):
    """Пошук книжок"""

    def get_queryset(self):
        return Book.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context
