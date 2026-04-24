from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="tester@example.com", password="strongpass123")

    def test_login_returns_access_and_refresh_tokens(self):
        url = reverse("login")
        response = self.client.post(url, {"email": "tester@example.com", "password": "strongpass123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], "tester@example.com")

    def test_register_creates_user(self):
        url = reverse("register")
        payload = {"email": "newuser@example.com", "password": "verystrong123"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        self.assertIn("access", response.data)
