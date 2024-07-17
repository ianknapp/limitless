from django.conf import settings
from django.db import models

from limitless.common.models import AbstractBaseModel
from limitless.utils.misc import datetime_appended_filepath


class Project(AbstractBaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    model_3d = models.FileField(upload_to=datetime_appended_filepath, blank=True, null=True)
    print_config = models.FileField(upload_to=datetime_appended_filepath, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-last_edited"]
