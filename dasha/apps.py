from django.apps import AppConfig


class DashaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dasha'

    def ready(self):
        import dasha.signals
