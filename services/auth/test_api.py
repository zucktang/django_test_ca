import json

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from apps.user.models import User
from apps.user.factories import UserFactory  

class AuthTokenTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(username='testuser', password='password123')
        
    def get_credential_dict_data(self, username, password):
        return {'username': username, 'password': password}

    def test_001_valid_login(self):
        data = self.get_credential_dict_data('testuser', 'password123')
        response = self.client.post('/api/auth/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user_id'], self.user.pk)
        self.assertEqual(response.data['email'], self.user.email)

    def test_002_invalid_login(self):
        data = self.get_credential_dict_data('testuser', 'wrongpassword')
        response = self.client.post('/api/auth/token/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"error": "Unable to login with provided credentials."})

    def test_003_missing_username(self):
        data = {'password': 'testpassword'}
        response = self.client.post('/api/auth/token/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Username and password are required"})

    def test_004_missing_password(self):
        data = {'username': 'testuser'}
        response = self.client.post('/api/auth/token/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Username and password are required"})