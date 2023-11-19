from django.contrib import admin
from .models import Book,Review,Rating

# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Rating)
