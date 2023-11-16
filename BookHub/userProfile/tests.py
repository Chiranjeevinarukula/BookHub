from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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
