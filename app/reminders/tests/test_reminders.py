# """ Test for the reminders API """
from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Reminder
from ..serializers import ReminderSerializer, ReminderDetailSerializer

REMINDERS_URL = reverse('reminders:reminders-list')


def detail_url(reminder_id):
    """ Create and return a URL for specific object """
    return reverse('reminders:reminders-detail', args=[reminder_id])


def date_to_string(date_type):
    return date_type.strftime('%Y-%m-%d')


def create_reminder(user, **kwargs):
    """ Create and return a test reminder """
    today = date.today()
    defaults = {
        'title': 'Test Reminder',
        'description': 'Test description.',
        'reminder_date': date(today.year + 1, today.month, today.day),
        'permanent': True
    }
    defaults.update(**kwargs)
    reminder = Reminder.objects.create(user=user, **defaults)
    return reminder


def create_user(**params):
    """ Create and return a test user """
    user = get_user_model().objects.create_user(**params)
    return user


class PublicRemindersAPITests(TestCase):
    """ Test unauthenticated API requests """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test authentication is required to call API """
        res = self.client.get(REMINDERS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """ Test authenticated API requests """

    def setUp(self):
        self.today = date.today()
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='Test1234')
        self.client.force_authenticate(self.user)

    def test_retrieve_reminders(self):
        """ Test retrieving a list of reminders works for authenticated users"""
        create_reminder(user=self.user)
        create_reminder(user=self.user)
        create_reminder(user=self.user)

        res = self.client.get(REMINDERS_URL)

        reminders = Reminder.objects.all()
        serializer = ReminderSerializer(reminders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_reminders_limited_to_a_user(self):
        """ Test retrieved reminders are limited to the authenticated user """
        other_user = create_user(email='other_user@example.com', password='Password1234')
        create_reminder(user=other_user)
        create_reminder(user=self.user)

        res = self.client.get(REMINDERS_URL)

        reminders = Reminder.objects.filter(user_id=self.user.id)
        serializer = ReminderSerializer(reminders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_specific_reminder(self):
        """ Test retrieving a specific reinder works """
        reminder = create_reminder(user=self.user)
        res = self.client.get(detail_url(reminder.id))

        serializer = ReminderDetailSerializer(reminder)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_reminder(self):
        """ Test creating a reminder works """
        payload = {
            'title': "Agatka's Birthday",
            'reminder_date': date(self.today.year + 1, 2, 27),
            'description': "Agatka's birthday yearly reminder.",
            'permanent': True
        }

        res = self.client.post(REMINDERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        reminder = Reminder.objects.get(id=res.data['id'])

        for key, value in payload.items():
            self.assertEqual(getattr(reminder, key), value)
        self.assertEqual(reminder.user, self.user)

    def test_delete_reminder(self):
        """ Test deleting a reminder """
        reminder = create_reminder(user=self.user)
        res = self.client.delete(detail_url(reminder.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reminder.objects.filter(id=reminder.id).exists())

    def test_deleting_someones_reminder_not_possible(self):
        """ Test deleting someone's else reminder is not possible """
        other_user = create_user(email='other_user@example.com')
        reminder = create_reminder(user=other_user)
        res = self.client.delete(detail_url(reminder.id))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Reminder.objects.filter(id=reminder.id).exists())

    def test_partial_update(self):
        """ Test patching a reminder """
        original_title = "Agatka's birthday"
        payload = {'reminder_date': date(self.today.year + 1, 2, 28)}
        reminder = create_reminder(user=self.user, title=original_title, reminder_date=date(self.today.year + 1, 2, 27))
        res = self.client.patch(detail_url(reminder.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        reminder.refresh_from_db()

        self.assertEqual(original_title, res.data['title'])
        self.assertEqual(reminder.reminder_date, payload['reminder_date'])
        self.assertEqual(reminder.user, self.user)

    def test_full_update(self):
        """ Test full update of a reminder """
        reminder = create_reminder(user=self.user)
        paylaod = {
            'title': 'Updated Title',
            'reminder_date': date(self.today.year + 1, 1, 1),
            'description': 'Updated Description',
        }
        res = self.client.put(detail_url(reminder.id), paylaod)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        reminder.refresh_from_db()
        for key, value in paylaod.items():
            self.assertEqual(getattr(reminder, key), value)
        self.assertEqual(reminder.permanent, False)
        self.assertEqual(reminder.user, self.user)

    def test_cannot_update_user_of_reminder(self):
        """ Test cannot change the user field of the reminder """
        new_user = create_user(email='new_user@example.com')
        reminder = create_reminder(user=self.user)

        self.client.patch(detail_url(reminder.id), {'user': new_user.id})
        reminder.refresh_from_db()

        # We don't assert status code since it will be 200, but serializer won't let changing user
        self.assertEqual(reminder.user, self.user)

    # def test_create_reminder_with_new_tags(self):
    #     """ Test creating a reminder with new tags """
    #     payload = {
    #         'title': "Agatka's Birthday",
    #         'reminder_date': date(self.today.year + 1, 1, 1),
    #         'tags': [{'name': 'Birthday'}, {'name': 'Important'}]
    #     }
    #
    #     res = self.client.post(REMINDERS_URL, payload, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #
    #     reminders = Reminder.objects.filter(user=self.user)
    #     self.assertEqual(len(reminders), 1)
    #
    #     reminder = reminders[0]
    #     self.assertEqual(reminder.tags.count(), 2)
    #
    #     for tag in payload['tags']:
    #         exists = Tag.objects.filter(name=tag['name'], user=self.user).exists()
    #         self.assertTrue(exists)
    #
    # def test_create_reminder_with_existing_tags(self):
    #     """ Test creating a reminder with existing tags """
    #     # Sprawdzić i usunąć, czy ten tag nie zostanie zwrócony w reminder.tags.all()
    #     other_user = create_user(email='some_other@example.com')
    #     Tag.objects.create(name='Some Tag', user=other_user)
    #
    #     tag = Tag.objects.create(name='Birthday', user=self.user)
    #     payload = {
    #         'title': "Agatka's Birthday",
    #         'reminder_date': date(self.today.year + 1, 1, 1),
    #         'tags': [{'name': 'Birthday'}, {'name': 'Important'}]
    #     }
    #
    #     res = self.client.post(REMINDERS_URL, payload, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #
    #     reminders = Reminder.objects.filter(user=self.user)
    #     self.assertEqual(len(reminders), 1)
    #
    #     reminder = reminders[0]
    #     self.assertEqual(len(reminder.tags), 2)  # Sprawdzić czy działa, czy musi być count()
    #     self.assertIn(tag, reminders.tags.all())
    #
    #     tags = Tag.objects.filter(user=self.user)
    #     self.assertEqual(len(tags), 2)
    #
    #     for tag in payload['tags']:
    #         exists = reminder.tags.filter(name=tag['name']).exists()
    #         self.assertTrue(exists)
    #
    # def test_create_tag_on_update(self):
    #     """ Test tag is created when reminder is updated """
    #     reminder = create_reminder(user=self.user)
    #     payload = {
    #         'tags': [{'name': 'Birthday'}]
    #     }
    #
    #     self.assertEqual(Tag.objects.count(), 0)
    #
    #     res = self.client.patch(detail_url(reminder.id), payload, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #
    #     new_tag = Tag.objects.get(user=self.user, name='Birthday')
    #     self.assertIn(new_tag, reminder.tags.all())
