import logging

from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from limitless.cura.models import CuraSettings
from limitless.cura.serializers import AllSettingsSerializer
from limitless.cura.settings import (
    AdhesionType,
    SupportStructure,
    SupportType,
    cura_settings_str,
)
from limitless.cura.tasks import slice_model

from .models import Printer, Project, ProjectFile
from .serializers import PrinterSerializer, ProjectDetailsSerializer, ProjectSerializer

logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Project.objects.filter(hidden=False)
    serializer_class = ProjectSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProjectDetailsSerializer(instance)
        return Response(serializer.data)


@api_view(["POST"])
def print(request):
    project = Project.objects.get(pk=request.data["pk"])
    printer = Printer.objects.get(pk=request.data["printer"])
    settings = CuraSettings()
    settings.enable_support = project.enable_support
    settings.infill_sparse_density = project.infill_sparse_density
    settings.support_structure = SupportStructure(request.data["support_structure"])
    settings.support_type = SupportType(request.data["support_type"])
    settings.adhesion_type = AdhesionType(request.data["adhesion_type"])
    stl_file = project.files.filter(file_type=ProjectFile.TypeChoices.MODEL).first()

    file_path = slice_model(stl_file, printer.slug, cura_settings_str(settings), request.data.get("minimize_supports", False))
    file_data = {}
    with open(file_path, "rb") as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type="application/gcode")
    response["Content-Disposition"] = f'attachment; filename="{file_path.name}"'
    return response


@api_view(["GET"])
def settings(request):
    # Return global setting options to inject into session storage
    data = AllSettingsSerializer("").data
    data["printers"] = PrinterSerializer(Printer.objects.all(), many=True).data
    return Response(data)
