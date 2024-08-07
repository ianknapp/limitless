import logging

from django.contrib import admin
from django.http import HttpResponse

from .models import Printer, Project, ProjectFile
from .tasks import slice_model

logger = logging.getLogger(__name__)


class ProjectFileInlineAdmin(admin.TabularInline):
    model = ProjectFile
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    change_form_template = "admin/build_project_form.html"
    list_display = ("title", "owner", "num_files", "hidden", "created")
    list_filter = ("hidden",)
    inlines = [ProjectFileInlineAdmin]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "owner",
                    "hidden",
                )
            },
        ),
        (
            "Custom Cura Settings",
            {"fields": ("enable_support", "support_type", "support_structure", "infill_sparse_density", "adhesion_type")},
        ),
    )

    def num_files(self, obj):
        return obj.files.count()

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        if not request.path.endswith("/add/"):
            # Only allow for slicing after creation
            extra_context["build_project"] = True
        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        if "_build_project" in request.POST:
            # For now just grab the first model file we find
            # TODO - update this
            file_path = slice_model(obj.files.filter(file_type=ProjectFile.TypeChoices.MODEL).first())
            logger.info(f"Returning file: {file_path.name}")
            file_data = {}
            with open(file_path, "rb") as f:
                file_data = f.read()
            response = HttpResponse(file_data, content_type="application/gcode")
            response["Content-Disposition"] = f'attachment; filename="{file_path.name}"'
            return response
        return super().response_change(request, obj)


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    change_form_template = "admin/s3_upload_form.html"
    list_display = ("title", "file", "file_type", "primary", "created")
    list_filter = ("file_type",)

    def title(self, obj):
        return obj.project.title


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "cura_managed", "hidden", "file")
    list_filter = ("cura_managed", "hidden")
