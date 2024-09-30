""" Validators for models """
from datetime import date
import calendar
from django.core.exceptions import ValidationError


# Reminder validators
def validate_reminder_date(reminder_date):
    today = date.today()
    # Check if the day of creating a reminder is a last day of the month
    _, num_of_days = calendar.monthrange(today.year, today.month)
    check_date = date(today.year, today.month, today.day + 1) if today.day < num_of_days else date(today.year, today.month + 1, 1)

    if reminder_date < check_date:
        raise ValidationError('Date cannot be set in the past and needs to be set at least at tomorrow.')
