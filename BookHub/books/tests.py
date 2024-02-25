from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseForbidden
from .models import Book,Review, Reply 
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import json

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




class ReviewReplyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='hp', password='password')
        self.book = Book.objects.create(
            user=self.user,
            title='Test Title',
            author='Test Author',
            isbn='1234567890123',
            cover_image='path/to/cover.jpg',
            genre='Test Genre'
        )
        self.review = Review.objects.create(
            reviewedUser=self.user,
            book=self.book,
            review="Great book, highly recommended."
        )
        self.reply1 = Reply.objects.create(
            repliedUser=self.user,
            review=self.review,
            reply="testing reply"
        )
        self.reply2 = Reply.objects.create(
            repliedUser=self.user,
            review=self.review,
            reply="Yeah correct"
        )
        self.client = APIClient()

    def test_get_replies(self):
        url = reverse('getrepliesapi', args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)

        expected_data = [
            {
                "id": self.reply1.id,
                "reply": "testing reply",
                "created_at": self.reply1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "repliedUser": "hp",
                "review": "Great book, highly recommended."
            },
            {
                "id": self.reply2.id,
                "reply": "Yeah correct",
                "created_at": self.reply2.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "repliedUser": "hp",
                "review": "Great book, highly recommended."
            }
        ]
        self.maxDiff = None
        self.assertEqual(response_data, expected_data)

class ReviewReplyPostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='hp', password='password')
        self.book = Book.objects.create(
            user=self.user,
            title='Test Title',
            author='Test Author',
            isbn='1234567890123',
            cover_image='path/to/cover.jpg',
            genre='Test Genre'
        )
        self.review = Review.objects.create(
            reviewedUser=self.user,
            book=self.book,
            review="Great book, highly recommended."
        )
        self.client = APIClient()
    def test_create_review_reply_without_login(self):
        data = {
            "reply": "testing reply",
            "review": self.review.id,
            "repliedUser":self.user.id,
        }
        url = '/books/review/reply/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn('/accounts/login/', response.url)

    def test_create_review_reply(self):
        self.client.force_login(self.user)
        data = {
            "reply": "testing reply",
            "review": self.review.id,
            "repliedUser":self.user.id,
        }
        url = '/books/review/reply/'
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_data = {
            "id": response.data["id"],
            "reply": "testing reply",
            "created_at": response.data["created_at"],
            "repliedUser": "hp",
            "review": "Great book, highly recommended."
        }

        self.assertEqual(response.data, expected_data)
        self.assertTrue(Reply.objects.filter(id=response.data["id"]).exists())


class ReviewDeleteTestCase(TestCase):
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
        self.review = Review.objects.create(
            reviewedUser=self.user,
            book=self.book,
            review="Great book, highly recommended."
        )
        self.url = reverse('reviewDelete', args=[self.review.pk])

    def test_review_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        initial_review_count = self.book.review.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())
        self.assertEqual(self.book.review.count(), initial_review_count - 1)
        print(response.content.decode())
        expected_url = reverse('detail_book', args=[self.book.id])
        self.assertRedirects(response, expected_url)

    def test_review_delete_view_unauthenticated_user(self):
        initial_review_count = self.book.review.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content.decode(), "Cannot delete other's review")
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())
        self.assertEqual(self.book.review.count(), initial_review_count)

class AdminDeleteBookTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.user = User.objects.create_user(username='user', password='userpass', email='user@example.com')
        self.book = Book.objects.create(
            user=self.user,
            title='Test Title',
            author='Test Author',
            isbn='1234567890123',
            cover_image='path/to/cover.jpg',
            genre='Test Genre'
        )

    def test_delete_book_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(reverse('deleteBook', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=self.book.id)

    def test_delete_book_as_unauthority(self):
        response = self.client.delete(reverse('deleteBook', args=[self.book.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())

class AdminUpdateBookTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.user = User.objects.create_user(username='user', password='userpass', email='user@example.com')
        self.book = Book.objects.create(
            user=self.user,
            title='Test Title',
            author='Test Author',
            isbn='1234567890123',
            cover_image='path/to/cover.jpg',
            genre='Test Genre'
        )

    def test_delete_book_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        updated_data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'isbn': '9876543210987',
            'cover_image': 'path/to/updated_cover.jpg',
            'genre': 'Updated Genre'
        }
        response = self.client.post(reverse('update_book', args=[self.book.id]),data=updated_data)

        self.assertEqual(response.status_code, 302)
        updated_book = Book.objects.get(id=self.book.id)
        self.assertEqual(updated_book.title, 'Updated Title')
        self.assertEqual(updated_book.author, 'Updated Author')
        self.assertEqual(updated_book.isbn, '9876543210987')
        self.assertEqual(updated_book.genre, 'Updated Genre')

    def test_delete_book_as_unauthority(self):
        response = self.client.delete(reverse('deleteBook', args=[self.book.id]))
        self.assertEqual(response.status_code, 403)
        updated_book = Book.objects.get(id=self.book.id)
        self.assertEqual(updated_book.title, self.book.title)
        self.assertEqual(updated_book.author, self.book.author)

class ReviewDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.superuser = User.objects.create_superuser(username='adminuser', password='adminpassword', email='admin@example.com')
        self.book = Book.objects.create(
            user=self.user,
            title='Test Title',
            author='Test Author',
            isbn='1234567890123',
            cover_image='path/to/cover.jpg',
            genre='Test Genre'
        )
        self.review = Review.objects.create(
            reviewedUser=self.user,
            book=self.book,
            review="Great book, highly recommended."
        )
        self.url = reverse('reviewDelete', args=[self.review.pk])

    def test_delete_review_by_owner(self):
        self.client.login(username='testuser', password='testpassword')
        initial_count = Review.objects.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), initial_count - 1)

    def test_delete_review_by_non_owner(self):
        non_owner = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        initial_count = Review.objects.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Review.objects.count(), initial_count)
        self.assertEqual(response.content.decode('utf-8'), "Cannot delete other's review")
    
    def test_delete_review_by_superuser(self):
        self.client.login(username='adminuser', password='adminpassword')
        initial_count = Review.objects.count()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), initial_count - 1)
