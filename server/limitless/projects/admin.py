import logging

from django.contrib import admin
from django.http import HttpResponse

from .models import Project
from .tasks import slice_model

logger = logging.getLogger(__name__)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    change_form_template = "admin/build_project_form.html"
    list_display = ("owner", "title", "model_3d", "print_config")

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        if not request.path.endswith("/add/"):
            # Only allow for slicing after creation
            extra_context["build_project"] = True
        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        if "_build_project" in request.POST:
            file_path = slice_model(obj)

            file_name = file_path.stem[:-18]
            logger.info(f"Returning file: {file_name}")
            file_data = {}
            with open(file_path, "rb") as f:
                file_data = f.read()
            response = HttpResponse(file_data, content_type='application/gcode')
            response["Content-Disposition"] = f'attachment; filename="{file_name}"'
            return response
        return super().response_change(request, obj)
