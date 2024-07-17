from django.apps import AppConfig


class RemaindersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'remainders'

    def ready(self):
        from . import remainders_sender
        remainders_sender.start()
