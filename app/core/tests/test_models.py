from django.test import TestCase

from django.contrib.auth import get_user_model
from decimal import Decimal
from core.models import Recipe,Tag


def create_user(email='user@example.com',password='testpass123'):
    return get_user_model().objects.create_user(email,password)

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successfull(self):
        """Test creating a user with email and password"""

        email = 'testexample@gmail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@Example.com','test1@example.com'],
            ['test2@EXample.com','test2@example.com'],
            ['test3@Example.Com','test3@example.com'],
            ['Test4@Example.com','test4@example.com']
                            ]
        
        for email,excepted in sample_emails:
            user = get_user_model().objects.create_user(email,'sample123')
            self.assertEqual(user.email,excepted)
    
    def test_new_user_without_email_raises_error(self):
        """Test the creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')
    

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        recipe = Recipe.objects.create(
            user = user,
            title = 'Sample recipe name',
            time_minutes = 4,
            price = Decimal('5.50'),
            description = 'Sample recipe description'
        )
    
        self.assertEqual(str(recipe),recipe.title)
    

    def test_create_tag(self):
        """Test creating a tag is successfull"""

        user = create_user()
        tag = Tag.objects.create(user=user,name='Tag1')

        self.assertEqual(str(tag),tag.name)

    
    


        
        
