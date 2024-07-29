import logging

from django.contrib import admin
from django.http import HttpResponse

from .models import Project, ProjectFile
from .tasks import slice_model

logger = logging.getLogger(__name__)


class ProjectFileInlineAdmin(admin.TabularInline):
    change_form_template = "admin/s3_upload_form.html"
    model = ProjectFile
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    change_form_template = "admin/build_project_form.html"
    list_display = ("title", "owner", "num_files", "created")
    inlines = [ProjectFileInlineAdmin]

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
    list_display = ("title", "file", "file_type", "created")
    list_filter = ("file_type",)

    def title(self, obj):
        return obj.project.title
