# """ Test for the remainders API """
from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Remainder
from ..serializers import RemainderSerializer

REMAINDERS_URL = reverse('remainders:remainders-list')


def detail_url(remainder_id):
    """ Create and return a URL for specific object """
    return reverse('remainders:remainders-detail', args=[remainder_id])


def date_to_string(date_type):
    return date_type.strftime('%Y-%m-%d')


def create_remainder(user, **kwargs):
    """ Create and return a test remainder """
    today = date.today()
    defaults = {
        'title': 'Test Remainder',
        'description': 'Test description.',
        'remainder_date': date(today.year + 1, today.month, today.day),
        'permanent': True
    }
    defaults.update(**kwargs)
    remainder = Remainder.objects.create(user=user, **defaults)
    return remainder


def create_user(**params):
    """ Create and return a test user """
    user = get_user_model().objects.create_user(**params)
    return user


class PublicRemaindersAPITests(TestCase):
    """ Test unauthenticated API requests """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test authentication is required to call API """
        res = self.client.get(REMAINDERS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """ Test authenticated API requests """

    def setUp(self):
        self.today = date.today()
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='Test1234')
        self.client.force_authenticate(self.user)

    def test_retrieve_remainders(self):
        """ Test retrieving a list of remainders works for authenticated users"""
        create_remainder(user=self.user)
        create_remainder(user=self.user)
        create_remainder(user=self.user)

        res = self.client.get(REMAINDERS_URL)

        remainders = Remainder.objects.all()
        serializer = RemainderSerializer(remainders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_remainders_limited_to_a_user(self):
        """ Test retrieved remainders are limited to the authenticated user """
        other_user = create_user(email='other_user@example.com', password='Password1234')
        create_remainder(user=other_user)
        create_remainder(user=self.user)

        res = self.client.get(REMAINDERS_URL)

        remainders = Remainder.objects.filter(user_id=self.user.id)
        serializer = RemainderSerializer(remainders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_specific_remainder(self):
        """ Test retrieving a specific remainder works """
        remainder = create_remainder(user=self.user)
        res = self.client.get(detail_url(remainder.id))

        serializer = RemainderSerializer(remainder)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_remainder(self):
        """ Test creating a remainder works """
        payload = {
            'title': "Agatka's Birthday",
            'remainder_date': date(self.today.year + 1, 2, 27),
            'description': "Agatka's birthday yearly remainder.",
            'permanent': True
        }

        res = self.client.post(REMAINDERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        remainder = Remainder.objects.get(id=res.data['id'])

        for key, value in payload.items():
            self.assertEqual(getattr(remainder, key), value)
        self.assertEqual(remainder.user, self.user)

    def test_delete_remainder(self):
        """ Test deleting a remainder """
        remainder = create_remainder(user=self.user)
        res = self.client.delete(detail_url(remainder.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Remainder.objects.filter(id=remainder.id).exists())

    def test_deleting_someones_remainder_not_possible(self):
        """ Test deleting someone's else remainder is not possible """
        other_user = create_user(email='other_user@example.com')
        remainder = create_remainder(user=other_user)
        res = self.client.delete(detail_url(remainder.id))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Remainder.objects.filter(id=remainder.id).exists())

    def test_partial_update(self):
        """ Test patching a remainder """
        original_title = "Agatka's birthday"
        payload = {'remainder_date': date(self.today.year + 1, 2, 28)}
        remainder = create_remainder(user=self.user, title=original_title, remainder_date=date(self.today.year + 1, 2, 27))
        res = self.client.patch(detail_url(remainder.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        remainder.refresh_from_db()

        self.assertEqual(original_title, res.data['title'])
        self.assertEqual(remainder.remainder_date, payload['remainder_date'])
        self.assertEqual(remainder.user, self.user)

    def test_full_update(self):
        """ Test full update of a remainder """
        remainder = create_remainder(user=self.user)
        paylaod = {
            'title': 'Updated Title',
            'remainder_date': date(self.today.year + 1, 1, 1),
            'description': 'Updated Description',
        }
        res = self.client.put(detail_url(remainder.id), paylaod)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        remainder.refresh_from_db()
        for key, value in paylaod.items():
            self.assertEqual(getattr(remainder, key), value)
        self.assertEqual(remainder.permanent, False)
        self.assertEqual(remainder.user, self.user)

    def test_cannot_update_user_of_remainder(self):
        """ Test cannot change the user field of the remainder """
        new_user = create_user(email='new_user@example.com')
        remainder = create_remainder(user=self.user)

        self.client.patch(detail_url(remainder.id), {'user': new_user.id})
        remainder.refresh_from_db()

        # We don't assert status code since it will be 200, but serializer won't let changing user
        self.assertEqual(remainder.user, self.user)
