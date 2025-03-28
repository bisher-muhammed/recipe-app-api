from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin"""

    def setUp(self):
        """Create a superuser and a normal user for testing"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='bisherp297@gmail.com',
            password='123',
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='user@example.com',  # Fixed email format
            password='testpassword',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed in the admin page"""
        url = reverse('admin:core_user_changelist')  # Ensure your custom User model is registered with 'core_user'
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)


    def test_edit_user_page(self):
        url = reverse('admin:core_user_change',args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
    

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)
