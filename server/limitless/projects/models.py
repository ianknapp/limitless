from django.conf import settings
from django.db import models

from limitless.common.models import AbstractBaseModel
from limitless.utils.misc import datetime_appended_filepath


class Project(AbstractBaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-last_edited"]


class ProjectFile(AbstractBaseModel):
    class TypeChoices(models.TextChoices):
        MODEL = "MODEL", "3D Model (STL, etc.)"
        IMAGE = "IMAGE", "Picture"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=datetime_appended_filepath)
    file_type = models.CharField(max_length=24, choices=TypeChoices.choices, blank=True, null=True)
    print_config = models.FileField(upload_to=datetime_appended_filepath, blank=True, null=True)

    def save(self, *args, **kwargs):
        file_ext = self.file.name.split(".")[-1].lower()
        if file_ext == "stl":
            self.file_type = self.TypeChoices.MODEL
        elif file_ext in ["png", "jpg", "jpeg"]:
            self.file_type = self.TypeChoices.IMAGE
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.title}: {self.file.name}"

    class Meta:
        ordering = ["-last_edited"]
