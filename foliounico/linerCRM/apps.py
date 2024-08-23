from django.apps import AppConfig


class LinerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'linerCRM'

    def ready(self):
        import linerCRM.signals