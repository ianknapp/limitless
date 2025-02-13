from django.db import models

from limitless.common.models import AbstractBaseModel

from .settings import AdhesionType, SupportStructure, SupportType


class CuraSettings(AbstractBaseModel):
    enable_support = models.BooleanField(default=False)
    support_type = models.CharField(max_length=255, choices=SupportType.choices, default=SupportType.EVERYWHERE)
    support_structure = models.CharField(max_length=255, choices=SupportStructure.choices, default=SupportStructure.NORMAL)
    infill_sparse_density = models.IntegerField(default=50, help_text="Infill percentage - used to calculate infill settings.")
    adhesion_type = models.CharField(max_length=255, choices=AdhesionType.choices, default=AdhesionType.NONE)
    layer_height = models.FloatField(default=0.2)
    initial_layer_height = models.FloatField(default=0.3)

    def __str__(self):
        owner = "n/a"
        if hasattr(self, "project"):
            owner = self.project
        if hasattr(self, "user"):
            owner = self.user
        return f"{owner} Cura Settings"

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "Cura Settings"
