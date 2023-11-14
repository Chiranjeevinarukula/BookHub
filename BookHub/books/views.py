from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Book,Review
from django.shortcuts import reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm

# Create your views here.
class books_listview(ListView):
    model = Book
    template_name = 'books/get_books.html'
    context_object_name = 'books'

class book_detailview(DetailView):
    model = Book
    template_name='books/detail_book.html'
    context_object_name = 'book'

class reviewCreate(LoginRequiredMixin,View):
    template_name = 'books/detail_book.html'
    def post(self,request,bookId):
        form=ReviewForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)  # Create a Review instance but don't save it yet
            data.reviewedUser = request.user
            data.book_id = bookId  # Assuming you have a 'book' field in your Review model
            data.save()
            return HttpResponseRedirect(reverse('detail_book', args=(bookId,)))
        else:
            return HttpResponseRedirect(reverse('detail_book', args=(bookId,)))