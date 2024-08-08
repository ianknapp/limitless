from django.db import models

from .settings import AdhesionType, SupportStruture, SupportType


class AbstractCuraSettingsModel(models.Model):
    """
    Settings needed for slicing a print
    Projects/Files/Printers might have different preferred defaults
    Users may also want to override those defaults
    """

    enable_support = models.BooleanField(default=False)
    support_type = models.CharField(max_length=255, choices=SupportType.choices, default=SupportType.EVERYWHERE)
    support_structure = models.CharField(max_length=255, choices=SupportStruture.choices, default=SupportStruture.NORMAL)
    infill_sparse_density = models.IntegerField(default=50, help_text="Infill percentage - used to calculate infill settings.")
    adhesion_type = models.CharField(max_length=255, choices=AdhesionType.choices, default=AdhesionType.NONE)

    class Meta:
        abstract = True

    def __str__(self):
        return "ah yes"


class SettingsData(AbstractCuraSettingsModel):
    class Meta:
        managed = False
