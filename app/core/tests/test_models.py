""" Tests for models """
from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from ..models import Remainder


class ModelTests(TestCase):
    """ Test models """

    def test_create_user_with_email_successful(self):
        """ Test creating a user with an email is successful """
        email = 'test@example.com'
        password = 'test1234'
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password), password)

    def test_new_user_email_normalized(self):
        """ Test email is normalized for new users """
        sample_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@Example.Com', 'Test2@example.com'],
            ['TEST3@EXample.com', 'TEST3@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email, password='test1234')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test creating a user without an email raises a ValueError """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='test1234')

    def test_create_superuser(self):
        """ Test creating a superuser """
        user = get_user_model().objects.create_superuser(email='superuser@example.com', password='test1234', name='Test User')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_remainder(self):
        """ Test creating a remainder """
        user = get_user_model().objects.create_user(email='test@example.com', password='Test1234')
        current_year = date.today().year
        remainder = Remainder.objects.create(
            title='Test Remainder',
            description='Test Description',
            remainder_date=date(current_year + 1, 1, 1),
            permanent='True',
            user=user
        )

        self.assertEqual(str(remainder), remainder.title)
        self.assertEqual(remainder.sent_check, 'None')
