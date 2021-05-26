from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    name = 'api'

    def ready(self):
        import api.signals
