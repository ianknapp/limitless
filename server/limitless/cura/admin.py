from django.contrib import admin

from limitless.cura.models import CuraSettings


@admin.register(CuraSettings)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["owner", "enable_support", "support_type", "support_structure", "infill_sparse_density", "adhesion_type"]

    def owner(self, obj):
        if hasattr(obj, "owner"):
            return obj.owner
        return "n/a"
