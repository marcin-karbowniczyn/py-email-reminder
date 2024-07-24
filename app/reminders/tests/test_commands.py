""" Tests for remanders commands """
from datetime import date

from django.core.management import call_command
from django.test import TestCase
from django.core.management import CommandError

from core.models import Reminder


class CommandsTest(TestCase):
    """ Test reminders commands """

    def setUp(self):
        self.today = date.today()

    def test_command_without_options_returns_error(self):
        """ Test using command without --past or --today returns Command Error """
        with self.assertRaises(CommandError):
            call_command('create_reminder')

    def test_command_past_creates_reminder_in_the_past(self):
        """ Test --past option creates reminder set in the past """
        call_command('create_reminder', '--past')
        reminder = Reminder.objects.all()[0]

        self.assertTrue(reminder.reminder_date < self.today)

    def test_command_today_creates_reminder_today(self):
        """ Test --today option creates reminder set on today """
        call_command('create_reminder', '--today')
        reminder = Reminder.objects.all()[0]

        self.assertEqual(reminder.reminder_date, self.today)
