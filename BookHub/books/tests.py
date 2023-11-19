from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseForbidden
from .models import Book

class UpdateBookTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(
            user=self.user,
            title='Test Title',
            author='Test Author',
            isbn='1234567890123',
            cover_image='path/to/cover.jpg',
            genre='Test Genre'
        )

    def test_update_book_view_authority(self):
        self.client.login(username='testuser', password='testpassword')
        updated_data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'isbn': '9876543210987',
            'cover_image': 'path/to/updated_cover.jpg',
            'genre': 'Updated Genre'
        }
        response = self.client.post(reverse('update_book', args=[self.book.id]), data=updated_data)
        self.assertRedirects(response, reverse('get_books'))
        updated_book = Book.objects.get(id=self.book.id)
        self.assertEqual(updated_book.title, 'Updated Title')
        self.assertEqual(updated_book.author, 'Updated Author')
        self.assertEqual(updated_book.isbn, '9876543210987')
        self.assertEqual(updated_book.genre, 'Updated Genre')

    def test_update_book_view_no_authority(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.post(reverse('update_book', args=[self.book.id]), data={'title': 'Updated Title'})
        self.assertIsInstance(response, HttpResponseForbidden)
        updated_book = Book.objects.get(id=self.book.id)
        self.assertNotEqual(updated_book.title, 'Updated Title')


class DeleteBookTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(
            user=self.user,
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            cover_image='path/to/cover.jpg',
            genre='Test Genre'
        )

    def test_delete_book_view_authority(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('deleteBook', args=[self.book.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('get_books'))

        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=self.book.id)

    def test_delete_book_view_no_authority(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        url = reverse('deleteBook', args=[self.book.id])
        response = self.client.post(url)
        self.assertIsInstance(response, HttpResponseForbidden)