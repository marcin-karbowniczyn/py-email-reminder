""" Validators for models """
from datetime import date
from django.core.exceptions import ValidationError


# Remainder validators
def validate_remainder_date(remainder_date):
    today = date.today()
    if remainder_date < date(today.year, today.month, today.day + 1):
        raise ValidationError('Date cannot be set in the past and needs to be set at least at tomorrow.')
