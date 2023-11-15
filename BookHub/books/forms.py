from django import forms
from .models import Review,Rating,Book

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields=['review']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']

class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields=['title','author','isbn','genre','cover_image']