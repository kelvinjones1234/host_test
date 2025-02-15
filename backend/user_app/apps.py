from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'
    verbose_name = 'Users'

    def ready(self):
        import user_app.signals

