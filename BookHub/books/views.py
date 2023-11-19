from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView
from .models import Book,Review,Rating
from django.shortcuts import reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm,RatingForm,BookForm
from django.urls import reverse_lazy

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
    print('hey')
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
        
class ratingCreate(LoginRequiredMixin,View):
    template_name = 'books/detail_book.html'
    def post(self,request,bookId):
        print('calling')
        try:
            rating = Rating.objects.get(ratedUser__id = request.user.id ,book__id = bookId)
            form = RatingForm(request.POST,instance=rating)
            form.save()
            return HttpResponseRedirect(reverse('detail_book',args=(bookId,)))
        except Rating.DoesNotExist:
            form=RatingForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)  
                data.ratedUser = request.user
                data.book_id = bookId  
                data.save()
                return HttpResponseRedirect(reverse('detail_book', args=(bookId,)))
            else:
                return HttpResponseRedirect(reverse('detail_book', args=(bookId,))) 
        
class CreateBookView(LoginRequiredMixin,CreateView):
    model = Book
    template_name='books/postbook.html'
    form_class = BookForm
    success_url=reverse_lazy('get_books')

    def form_valid(self, form):
        # Automatically set the user and book for the comment
        form.instance.user = self.request.user
        return super().form_valid(form)