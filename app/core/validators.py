""" Validators for models """
from datetime import date
from django.core.exceptions import ValidationError


# Reminder validators
def validate_reminder_date(reminder_date):
    today = date.today()
    if reminder_date < date(today.year, today.month, today.day + 1):
        raise ValidationError('Date cannot be set in the past and needs to be set at least at tomorrow.')
