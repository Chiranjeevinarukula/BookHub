from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    isbn = models.CharField(max_length=13, unique=True)
    cover_image = models.ImageField(upload_to='images/')
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
    def get_rating_values(self):
        return self.rating.values_list('rating', flat=True)
    

class Review(models.Model):
    reviewedUser = models.ForeignKey(User, related_name='review', on_delete=models.CASCADE)
    review = models.TextField(max_length=250,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book,related_name='review',on_delete=models.CASCADE)

    def __str__(self):
        return self.review

class Rating(models.Model):
    book = models.ForeignKey(Book,related_name='rating',on_delete=models.CASCADE,null=True)
    ratedUser = models.ForeignKey(User, related_name='rating', on_delete=models.CASCADE,null=True)
    rating = models.IntegerField(
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )