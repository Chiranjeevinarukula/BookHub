from django.shortcuts import render
from django.views.generic import ListView
from .models import Book

# Create your views here.
class books_listview(ListView):
    model = Book
    template_name = 'books/get_books.html'
    context_object_name = 'books'