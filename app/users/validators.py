import re
from django.core.exceptions import ValidationError


class NumericInPasswordCustomValidator:
    def __init__(self, min_digits=1):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if len(re.findall(r"\d", password)) < self.min_digits:
            raise ValidationError(
                'This password must contain at least %(min_digits)d digits.',
                code='password_no_digit',
                params={'min_digits': self.min_digits}
            )

    def get_help_text(self):
        return f'Your password must contain at least %(min_digits)d digits.' % {'min_digits': self.min_digits}


class AtLeastOneCapitalLetterCustomValidator:
    def validate(self, password, user=None):
        if len(re.findall("[A-Z]", password)) < 1:
            # Standard way of raising errors with serializers, if we raise the error, view translates it into HTTP 400 bad request reponse
            raise ValidationError(
                'This password must contain at least 1 capital letter.',
                code='password_no_capital_letters'
            )

    def get_help_text(self):
        return f'Your password must contain at least 1 digits.'
