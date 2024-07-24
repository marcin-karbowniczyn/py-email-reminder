""" Django command to create reminders in the past or for today """
from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError

from core.models import Reminder, User


class Command(BaseCommand):
    """ Django command to create a reminder in the past or for today """

    def add_arguments(self, parser):
        """ Add future, past or today option """
        parser.add_argument('--past', action='store_true', help="Create a reminder set in the past.")
        parser.add_argument('--today', action='store_true', help="Create a reminder with today's date.")
        parser.add_argument('--permanent', action='store_true', help="Create a reminder with permanent set to True.")

    def handle(self, *args, **options):
        """ Entrypoint for command """
        if not options['past'] and not options['today']:
            raise CommandError('You need to specify either --past or --today option for this command.')

        today = date.today()
        user, created = User.objects.get_or_create(email='command_test@example.com', name='Test User')

        reminder_options = {
            'user': user,
            'title': 'Test Reminder',
            'description': 'Test description.',
        }

        if options['permanent']:
            reminder_options['permanent'] = True

        if options['past']:
            reminder_options['reminder_date'] = today - timedelta(days=1)
            reminder_options.update({'title': 'Test past reminder'})

        if options['today']:
            reminder_options['reminder_date'] = today
            reminder_options.update({'title': 'Test today reminder'})

        Reminder.objects.create(**reminder_options)
        self.stdout.write(self.style.SUCCESS('Reminder has been created.'))
