""" Tests for remainders commands """
from datetime import date

from django.core.management import call_command
from django.test import TestCase
from django.core.management import CommandError

from core.models import Remainder


class CommandsTest(TestCase):
    """ Test remainders commands """

    def setUp(self):
        self.today = date.today()

    def test_command_without_options_returns_error(self):
        """ Test using command without --past or --today returns Command Error """
        with self.assertRaises(CommandError):
            call_command('create_remainder')

    def test_command_past_creates_remainder_in_the_past(self):
        """ Test --past option creates remainder set in the past """
        call_command('create_remainder', '--past')
        remainder = Remainder.objects.all()[0]

        self.assertTrue(remainder.remainder_date < self.today)

    def test_command_past_creates_remainder_today(self):
        """ Test --today option creates remainder set on today """
        call_command('create_remainder', '--today')
        remainder = Remainder.objects.all()[0]

        self.assertEqual(remainder.remainder_date, self.today)
