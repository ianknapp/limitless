from django.conf import settings
from django.db import models

from limitless.common.models import AbstractBaseModel
from limitless.cura.models import CuraSettings
from limitless.utils.misc import datetime_appended_filepath


class Project(AbstractBaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    settings = models.OneToOneField(CuraSettings, on_delete=models.SET_NULL, blank=True, null=True, related_name="project")
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hidden = models.BooleanField(default=True)

    def delete(self):
        if self.settings:
            self.settings.delete()
        super().delete()

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
    primary = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.file_type:
            # Ony on initial creation
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


class Printer(AbstractBaseModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True, null=True)
    cura_managed = models.BooleanField(default=True)
    file = models.FileField(upload_to=datetime_appended_filepath, blank=True, null=True)
    config_tweaks = models.TextField(blank=True, null=True)
    hidden = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class UserProfile(AbstractBaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    minimize_supports = models.BooleanField(default=False)
    printer = models.ForeignKey(Printer, on_delete=models.SET_NULL, null=True, related_name="user_profiles")

    def __str__(self):
        return self.user.email if self.user else "n/a"

    class Meta:
        ordering = ["-last_edited"]
