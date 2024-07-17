from django.contrib import admin

from .models import Project
from .tasks import slice_model


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    change_form_template = "admin/build_project_form.html"
    list_display = ("owner", "title", "model_3d", "print_config")

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["build_project"] = True
        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        if "_build_project" in request.POST:
            slice_model(obj)
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if "_build_project" in request.POST:
            slice_model(obj)
        return super().response_change(request, obj)
