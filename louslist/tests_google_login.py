from django.test import TestCase
from django.contrib.auth.models import User

class GoogleLoginTests(TestCase):
    def setUp(self):
        credentials = {"username": "test_username", "password": "test_password"}
        self.credentials = credentials
        User.objects.create_user(self.credentials)
    
    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.status_code == 200)
