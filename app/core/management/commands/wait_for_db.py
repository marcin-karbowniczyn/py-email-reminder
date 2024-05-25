""" Django command to wait for the database to be available """
import time

# The error that's thrown from the Psycopg2 package sometimes when the DB isn't ready
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """ Django comman to wait for the database """

    def handle(self, *args, **options):
        """ Entrypoint for command """
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (OperationalError, Psycopg2Error):
                self.stderr.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
