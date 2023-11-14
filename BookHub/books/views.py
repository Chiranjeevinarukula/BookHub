from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Book

# Create your views here.
class books_listview(ListView):
    model = Book
    template_name = 'books/get_books.html'
    context_object_name = 'books'

class book_detailview(DetailView):
    model = Book
    template_name='books/detail_book.html'
    context_object_name = 'book'
