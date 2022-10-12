from django.test import TestCase
from django.forms import ValidationError
from django.db.utils import DataError, IntegrityError

from accounts.models import User


class UserModelTest(TestCase):
    
    def setUp(self):
        self.user = User(username='test', email='test@mail.com', password='thisistest')
        self.user.save()

    
    def test_can_create_user_properly(self):
        self.assertEqual(self.user.username, 'test')
        self.assertEqual(self.user.email, 'test@mail.com')
        self.assertEqual(self.user.password, 'thisistest')

    
    def test_user_is_not_staff_by_default(self):
        self.assertFalse(self.user.is_staff)


    def test_user_is_not_superuser_by_default(self):
        self.assertFalse(self.user.is_superuser)


    def test_set_is_active_true_by_default(self):
        self.assertTrue(self.user.is_active)
    
    
    def test_cannot_create_user_with_empty(self):
        user = User()
        self.assertFalse(user.save())

    
    def test_username_cannot_over_150_characters(self):
        user2 = User(username='a'*151, email='test2@mail.com', password='thisistest')
        with self.assertRaises(ValidationError):
            user2.full_clean()


    def test_email_cannot_over_250_characters(self):
        user2 = User(username='test', email='t'*239 +
                     'test2@mail.com', password='thisistest')
        with self.assertRaises(ValidationError):
            user2.full_clean()


    def test_email_should_be_unique(self):
        user2 = User(username='test', email='test@mail.com',
                     password='thisistest')
        with self.assertRaises(IntegrityError):
            user2.save()

        
    