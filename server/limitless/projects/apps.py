from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "limitless.projects"

    def ready(self):
        # this import is required to register signals after the app is initialized
        # https://docs.djangoproject.com/en/4.1/topics/signals/
        from limitless.projects.signals import (  # noqa
            init_project_settings,
            init_user_profile,
        )

        return super().ready()
