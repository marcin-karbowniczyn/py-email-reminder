""" Tests for the users API """
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:signup')


def create_user(**params):
    """ Create and return a new user """
    return get_user_model().objects.create_user(**params)


class PublicUsersAPITests(TestCase):
    """ Test the public features of the users API """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ Test creating a user is successful """
        payload = {
            'email': 'testuser@example.com',
            'password': 'Test1234',
            'name': 'Test Name'  # Sprawdzić czy działa bez name
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """ Test an error returned if user with email exists """
        payload = {
            'email': 'test@example.com',
            'password': 'Test1234',
            'name': 'Test Name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, **payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_password_doesnt_meet_requiremenets(self):
        """ Test an error is returned when password haven't met requirements """
        passwords = [
            'testtest',
            'Testtest',
            'test1234',
        ]
        payload = {
            'email': 'test@example.com',
            'name': 'Test User'
        }

        for password in passwords:
            payload.update({'password': password})
            res = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            user_exists = get_user_model().objects.filter(email=payload['email']).exists()
            self.assertFalse(user_exists)

# class PrivateUsersAPITests(TestCase):
#     pass
