from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "limitless.core"

    def ready(self) -> None:
        # this import is required to register signals after the app is initialized
        # https://docs.djangoproject.com/en/4.1/topics/signals/
        from limitless.core.signals import create_auth_token_add_permissions  # noqa

        return super().ready()
