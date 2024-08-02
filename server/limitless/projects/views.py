import logging

from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Printer, Project, ProjectFile
from .serializers import PrinterSerializer, ProjectDetailsSerializer, ProjectSerializer
from .tasks import slice_model

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
    file_path = slice_model(
        project.files.filter(file_type=ProjectFile.TypeChoices.MODEL).first(),
        cura_settings_str=project.cura_settings_str,
    )
    file_data = {}
    with open(file_path, "rb") as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type="application/gcode")
    response["Content-Disposition"] = f'attachment; filename="{file_path.name}"'
    return response


@api_view(["GET"])
def printers(request):
    """
    On server startup:
        loop over cura/resources/definitions folder
        grab file name and the "name" attribute from each json file
        summarize as a json object and write to local cache (or file?)
    From here:
        Call a method that gets that dictionary from cache or calls method to load it
    Long term:
        When users save printer configs we'll need to save those to the DB anyway
        Maybe ignore cache and just write these to a DB table anyway?
        The values probably will never change
        If we install a new version of Cura that will likely just add options to the list
        If an option no longer exists...
            mark it as hidden on the DB
            manually upload it's config options to the DB
        We may want the ability to manually add extra or custom configs anyway
        So by default get_or_create all of them in the DB on server startup
        Maybe have a flag for "managed by cura"
        Those ones wouldn't have a file attached
        If we upload custom ones, then we'll need to also upload config files
        At slicer time we use these settings to pass the right path to Cura
    """
    serializer = PrinterSerializer(Printer.objects.all(), many=True)
    return Response(serializer.data)
