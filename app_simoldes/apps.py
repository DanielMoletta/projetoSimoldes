from django.apps import AppConfig

class AppSimoldesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_simoldes'
    def ready(self):
        import app_simoldes.signals