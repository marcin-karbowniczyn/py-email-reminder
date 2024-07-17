from django.apps import AppConfig


class RemaindersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'remainders'

    def ready(self):
        from . import manage_remainders
        manage_remainders.start()
