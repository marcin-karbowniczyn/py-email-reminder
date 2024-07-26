""" Database models """
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from core.validators import validate_reminder_date


# User Model
class UserManager(BaseUserManager):
    """ Manager for User Model """

    def create_user(self, email, password=None, **extra_fields):
        """ Create, save and return a new user """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, name):
        """ Create, save and return a superuser """
        user = self.create_user(email, password, name=name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Default User Model in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Only for superusers CLI


# Reminder Model
SENT_CHECKS = [
    ('None', 'None'),
    ('month', 'Month'),
    ('week', 'Week'),
    ('three_days', 'Three Days'),
    ('one_day', 'One Day'),
    ('today', 'Today'),
]


class Reminder(models.Model):
    """ Reminder object """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # I set the validation here for the django admin to be able to also call it, not only the serializer
    reminder_date = models.DateField(validators=[validate_reminder_date])
    permanent = models.BooleanField(default=False)
    sent_check = models.CharField(max_length=255, choices=SENT_CHECKS, default='None')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """ Tag object """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
