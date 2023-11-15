from django.contrib import admin
from .models import Book,Review,Rating,Reply

# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Reply)
