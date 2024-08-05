from django.conf import settings
from django.db import models

from limitless.common.models import AbstractBaseModel
from limitless.utils.misc import datetime_appended_filepath

from .cura_settings import (
    CuraSettingAdhesionType,
    CuraSettings,
    CuraSettingSupportStruture,
    CuraSettingSupportType,
    compute_infill_line_distance,
)


class Project(AbstractBaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hidden = models.BooleanField(default=True)

    # Custom Print Settings
    enable_support = models.BooleanField(default=False)
    support_type = models.CharField(max_length=255, choices=CuraSettingSupportType.choices, default=CuraSettingSupportType.EVERYWHERE)
    support_structure = models.CharField(
        max_length=255, choices=CuraSettingSupportStruture.choices, default=CuraSettingSupportStruture.NORMAL
    )
    infill_sparse_density = models.IntegerField(default=50, help_text="Infill percentage - used to calculate infill settings.")
    adhesion_type = models.CharField(max_length=255, choices=CuraSettingAdhesionType.choices, default=CuraSettingAdhesionType.NONE)

    def __str__(self):
        return self.title

    @property
    def cura_settings_str(self):
        settings = {
            CuraSettings.INFILL_LINE_DISTANCE: compute_infill_line_distance(self.infill_sparse_density),
            CuraSettings.SUPPORT_ENABLE: ("true" if self.enable_support else "false"),
            **(
                {
                    CuraSettings.SUPPORT_STRUCTURE: self.support_structure,
                    CuraSettings.SUPPORT_TYPE: self.support_type,
                }
                if self.enable_support
                else {}
            ),
            **({CuraSettings.ADHESION_TYPE: self.adhesion_type} if self.adhesion_type != CuraSettingAdhesionType.NONE else {}),
        }
        return " ".join(f"-s {key}={value}" for key, value in settings.items())

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
