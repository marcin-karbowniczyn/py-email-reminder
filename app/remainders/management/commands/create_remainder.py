""" Django command to create remainders in the past or for today """
from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError

from core.models import Remainder, User


class Command(BaseCommand):
    """ Django command to create a remainder in the past or for today """

    def add_arguments(self, parser):
        """ Add future, past or today option """
        parser.add_argument('--past', action='store_true', help="Create a remainder set in the past.")
        parser.add_argument('--today', action='store_true', help="Create a remainder with today's date.")
        parser.add_argument('--permanent', action='store_true', help="Create a remainder with permanent set to True.")

    def handle(self, *args, **options):
        """ Entrypoint for command """
        if not options['past'] and not options['today']:
            raise CommandError('You need to specify either --past or --today option for this command.')
            # self.stdout.write('You need to specify either --past or --today option for this command.')
            # return

        today = date.today()
        user, created = User.objects.get_or_create(email='command_test@example.com')

        remainder_options = {
            'user': user,
            'title': 'Test Remainder',
            'description': 'Test description.',
        }

        if options['permanent']:
            remainder_options['permanent'] = True

        if options['past']:
            remainder_options['remainder_date'] = today - timedelta(days=1)

        if options['today']:
            remainder_options['remainder_date'] = today

        Remainder.objects.create(**remainder_options)
        self.stdout.write(self.style.SUCCESS('Remainder has been created.'))
