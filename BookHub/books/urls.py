from django.urls import path
from . import views

urlpatterns = [
    path('',views.books_listview.as_view(),name='get_books'),
    path('<int:pk>/',views.book_detailview.as_view(),name = 'detail_book'),
]