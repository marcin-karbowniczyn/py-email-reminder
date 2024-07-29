""" Tests for the tags API """
from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Reminder, Tag
from reminders.serializers import TagSerializer

TAGS_URL = reverse('reminders:tags-list')


def detail_url(tag_id):
    """ Create and return a URL for
     detailed object """
    return reverse('reminders:tags-detail', args=[tag_id])


def create_user(email='user@example.com', password='Test1234'):
    """ Create and return a new test user """
    return get_user_model().objects.create_user(email, password)


class PublicTagsAPITests(TestCase):
    """ Test unauthenticated API requests """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """ Test authenticated API requests """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """ Test retrieving a list of tags """
        Tag.objects.create(name='Birthday', user=self.user)
        Tag.objects.create(name='Anniversary', user=self.user)

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """ Test list of tags is limited to the authenticated user """
        user2 = create_user('other_user@example.com', password='Test1234')
        Tag.objects.create(name='Birthday', user=user2)
        tag = Tag.objects.create(name='Anniversay', user=self.user)

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """ Test updating tag """
        payload = {
            'name': 'Anniversary'
        }

        tag = Tag.objects.create(name='Birthday', user=self.user)

        res = self.client.patch(detail_url(tag.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """ Test deleting a tag """
        tag = Tag.objects.create(name='Birthday', user=self.user)

        res = self.client.delete(detail_url(tag.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        tags = Tag.objects.filter(id=tag.id).exists()
        self.assertFalse(tags)

    def test_filter_tags_assigned_to_recipes(self):
        """ Test listing tags by those assigned to recipes """
        tag1 = Tag.objects.create(name='Birthday', user=self.user)
        tag2 = Tag.objects.create(name='Anniversary', user=self.user)

        today = date.today()
        reminder = Reminder.objects.create(
            title='Test Reminder',
            reminder_date=date(today.year + 1, 1, 1),
            user=self.user
        )
        reminder.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serialized_tag1 = TagSerializer(tag1)
        serialized_tag2 = TagSerializer(tag2)
        self.assertIn(serialized_tag1.data, res.data)
        self.assertNotIn(serialized_tag2.data, res.data)

    def test_filtered_tags_unique(self):
        """ Test filtered tags return a unique list """
        tag1 = Tag.objects.create(name='Birthday', user=self.user)
        Tag.objects.create(name='Anniversary', user=self.user)

        today = date.today()
        reminder1 = Reminder.objects.create(
            title="Dad's Birthday",
            reminder_date=date(today.year + 1, 1, 1),
            user=self.user
        )

        reminder2 = Reminder.objects.create(
            title="Mom's Birthday",
            reminder_date=date(today.year + 1, 2, 2),
            user=self.user
        )

        reminder1.tags.add(tag1)
        reminder2.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
