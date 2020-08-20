from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms
from .models import Book


class BookCreateForm(forms.ModelForm):
    """Форма створення книги"""
    class Meta:
        model = Book
        fields = '__all__'
