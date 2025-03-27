"""
Tests for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient  # ✅ Corrected import
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

TOKEN_URL = reverse('user:token')

ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)



class PublicApiTests(TestCase):
    """Tests for unauthenticated user API requests"""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)  # Ensure password is not in response

        
    
    def test_user_with_email_exists_error(self):  # ✅ Fixed typo
        """Test error returned if user with email already exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password is less than 5 characters"""
        payload = {
            'email': 'test123@gmail.com',
            'password': 'pw',  # Too short
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(  # ✅ Fixed typo
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
        self.assertIn('password', res.data)  # ✅ Ensure password error is returned

    

    def test_create_token_for_user(self):
        """Test generate token for valid credentials"""

        user_details = {
            'name':'Test name',
            'email':'test@example.com',
            'password':'test-user-password123'
        }
        create_user(**user_details)
        payload = {
            'email':user_details['email'],
            'password':user_details['password']
            
        }
        res = self.client.post(TOKEN_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
    

    def create_token_bad_credentials(self):
        create_user(email ='test@example.com',password='goodpass')
        payload = {'email':'test@example.com','password':'badpass'}
        
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    

    def test_create_token_blank_password(self):
        payload = {'email':'test@gmail.com','password':''}
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    

    def test_user_retrive_user_unotherized(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
    


class PrivateApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_profile_success(self):
        """Test retrieving profile for logged-in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me endpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the profile for the authenticated user"""
        payload = {'name': 'Updated Name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))  # ✅ Fix

        self.assertEqual(res.status_code, status.HTTP_200_OK)








    

    
