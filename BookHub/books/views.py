from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,DeleteView
from .models import Book,Review,Rating
from django.shortcuts import reverse
from django.views import View
from django.http import HttpResponseRedirect,HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm,RatingForm,BookForm
from django.urls import reverse_lazy
from django.db.models import Q 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReplySerializer
from django.contrib.auth.decorators import login_required

# Create your views here.
class books_listview(ListView):
    model = Book
    template_name = 'books/get_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        query = self.request.GET.get('query')

        if query:
            return Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(genre__icontains=query)
            )
        return Book.objects.all()
    
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
    
class UpdateBook(View):
    form_class=BookForm
    template_name = 'book/get_books.html'
    def post(self,request,bookId):
        book=Book.objects.get(id=bookId)
        if book.user != request.user:
            return HttpResponseForbidden('You dont have authority to change')
        form = BookForm(request.POST,instance=book)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('get_books'))
    
class OwnerMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.is_owner(obj):
            return HttpResponseForbidden("You don't have the required permissions to access this page.")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Book, pk=self.kwargs['pk'])  
    def is_owner(self, obj):
        return obj.user == self.request.user  

class DeleteBook(OwnerMixin,DeleteView):
    model=Book
    success_url = reverse_lazy('get_books')

@api_view(['GET'])
def getReplies(request,pk):
    replies = get_object_or_404(Review,id=pk)
    if(not replies):
       return Response(replies) 
    serializer = ReplySerializer(replies.reply,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@login_required
def CreateReply(request):
    if request.method == 'POST':
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
