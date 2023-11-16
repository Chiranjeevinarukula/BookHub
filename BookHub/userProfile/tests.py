from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import ProfileForm,UserForm
from django.http import HttpResponseForbidden
from .models import Profile

class ProfileViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_profile_view_returns_200(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('profile', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('profile', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'account/profile.html')

    def test_profile_view_displays_user_data(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('profile', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)

class ProfileUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('profileUpdate')

    def test_profile_update_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserForm)
        self.assertIsInstance(response.context['profileform'], ProfileForm)

    def test_profile_update_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, data={'username': 'newusername', 'email': 'newemail@example.com'})
        self.assertRedirects(response, reverse('profile', args=[self.user.pk]))
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.username, 'newusername')
        self.assertEqual(updated_user.email, 'newemail@example.com')

    def test_profile_update_view_post_invalid_data(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, data={'username': ''}) 
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserForm)
        self.assertIsInstance(response.context['profileform'], ProfileForm)
        self.assertTrue(response.context['form'].errors)
    
    def test_profile_update_post_unauthorized_user(self):
        response = self.client.post(self.url, data={'username': 'unauthroized'}) 
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content.decode(), "You do not have permission to edit this user.")
        self.assertIsInstance(response,HttpResponseForbidden)

# tests.py

# ... (existing imports)

class ProfileUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('profileUpdate')

    def test_profile_update_view_post_valid_data(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'profile_pic': 'path/to/image.jpg',  
            'bio': 'New bio',
            'favorite_genres': 'New genres',
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('profile', args=[self.user.pk]))
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.username, 'newusername')
        self.assertEqual(updated_user.email, 'newemail@example.com')

        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.bio, 'New bio')
        self.assertEqual(updated_profile.favorite_genres, 'New genres')
