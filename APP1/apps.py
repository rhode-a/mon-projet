from django.apps import AppConfig

class TonAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'APP1'

    def ready(self):
        import APP1.signals

