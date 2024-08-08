import logging

from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from limitless.cura.serializers import SettingsSerializer
from limitless.cura.settings import cura_settings_str
from limitless.cura.tasks import slice_model

from .models import Printer, Project, ProjectFile
from .serializers import PrinterSerializer, ProjectDetailsSerializer, ProjectSerializer

logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Project.objects.filter(hidden=False)
    serializer_class = ProjectSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # TODO - return the default setting selections for this project
        serializer = ProjectDetailsSerializer(instance)
        return Response(serializer.data)


@api_view(["POST"])
def print(request):
    project = Project.objects.get(pk=request.data["pk"])
    stl_file = project.files.filter(file_type=ProjectFile.TypeChoices.MODEL).first()
    printer = Printer.objects.get(pk=request.data["printer"])
    file_path = slice_model(stl_file, printer.slug, cura_settings_str(project))
    file_data = {}
    with open(file_path, "rb") as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type="application/gcode")
    response["Content-Disposition"] = f'attachment; filename="{file_path.name}"'
    return response


@api_view(["GET"])
def settings(request):
    # Return global setting options to inject into session storage
    data = SettingsSerializer("").data
    data["printers"] = PrinterSerializer(Printer.objects.all(), many=True).data
    return Response(data)
