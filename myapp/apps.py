from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"

    def ready(self):
        """
        Implement the ready method to import and register signals.
        This ensures that the signals are registered when the app is ready.
        """
        import myapp.signals
