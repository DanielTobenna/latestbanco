from django.apps import AppConfig


class HerculesbankappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'herculesbankapp'

    def ready(self):
    	import herculesbankapp.signals
