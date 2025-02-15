from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status

class ExchangeRateAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_exchange_rates(self):
        url = reverse('exchange_rates')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('rates', response.json())  # Adjust based on your API response structure

class UserAuthTests(APITestCase):
    def test_user_registration(self):
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post("/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        User.objects.create_user(username="testuser", password="testpass123")
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post("/auth/token/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())  # Ensure token is returned
  
class APITokenTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.tokens = None

    def test_reset_api_token(self):
        # First, obtain the initial tokens
        response = self.client.post("/auth/token/", {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        
        # Store the refresh token
        refresh_token = response.data["refresh"]
        
        # Now try to refresh the token
        response = self.client.post("/auth/token/refresh/", {
            "refresh": refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # Check for new access token
