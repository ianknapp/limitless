import logging

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import mixins, parsers, status, viewsets
from rest_framework.decorators import api_view, permission_classes, parser_classes
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

from .models import Filament, Printer, Project, ProjectFile
from .serializers import (
    FilamentSerializer,
    PrinterSerializer,
    ProjectCreationSerializer,
    ProjectDetailsSerializer,
    ProjectSerializer,
)

logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Project.objects.filter(hidden=False)
    serializer_class = ProjectSerializer

    def filter_queryset(self, queryset):
        search_query = self.request.query_params.get("search", "")
        recently_viewed = self.request.query_params.get("recently_viewed")

        if recently_viewed:
            queryset = queryset.filter(recently_viewed=True)
        if search_query:
            search_query = search_query.strip()
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        return queryset.distinct()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProjectDetailsSerializer(instance)
        return Response(serializer.data)


def is_image(f):
    if not isinstance(f, TemporaryUploadedFile):
        return False
    file_ext = f.content_type.split("/")[-1].lower()
    return file_ext in ["png", "jpeg", "gif", "svg"]


def is_3d_model(f):
    if not isinstance(f, TemporaryUploadedFile):
        return False
    file_ext = f.name.split(".")[-1].lower()
    return file_ext in ["stl"]


@api_view(["POST"])
@parser_classes([parsers.FormParser, parsers.MultiPartParser])
def create_project(request):
    serializer = ProjectCreationSerializer(data=request.data, context={"owner": request.user.pk})
    serializer.is_valid(raise_exception=True)
    project = serializer.save()
    primary_image = request.data.get("primaryImage")
    secondary_image = request.data.get("secondaryImage")
    model_file = request.data.get("model")
    if is_image(primary_image):
        ProjectFile.objects.create(project=project, file=primary_image, file_type=ProjectFile.TypeChoices.IMAGE, primary=True)
    if is_image(secondary_image):
        ProjectFile.objects.create(project=project, file=secondary_image, file_type=ProjectFile.TypeChoices.IMAGE)
    if is_3d_model(model_file):
        ProjectFile.objects.create(project=project, file=model_file, file_type=ProjectFile.TypeChoices.MODEL)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def my_projects(request):
    data = ProjectSerializer(request.user.projects.all(), many=True).data
    return Response(data)


@api_view(["DELETE"])
def delete_project(request, *args, **kwargs):
    project = Project.objects.get(pk=kwargs.get("pk"))
    if not project:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not (project.owner == request.user or request.user.is_staff):
        return Response(status=status.HTTP_403_FORBIDDEN)
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def print(request):
    project = Project.objects.get(pk=request.data["pk"])
    filament = Filament.objects.get(pk=request.data["filament"])
    printer = Printer.objects.get(pk=request.data["printer"]).slug
    settings = CuraSettings()
    settings.enable_support = project.settings.enable_support
    settings.infill_sparse_density = project.settings.infill_sparse_density
    settings.support_structure = SupportStructure(request.data["support_structure"])
    settings.support_type = SupportType(request.data["support_type"])
    settings.adhesion_type = AdhesionType(request.data["adhesion_type"])
    stl_file = project.files.filter(file_type=ProjectFile.TypeChoices.MODEL).first()

    file_path = slice_model(stl_file, filament.config, printer, cura_settings_str(settings), request.data.get("minimize_supports", False))
    file_data = {}
    with open(file_path, "rb") as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type="application/gcode")
    response["Content-Disposition"] = f'attachment; filename="{file_path.name}"'
    return response


@api_view(["GET"])
@permission_classes([])
def settings(request):
    # Return global setting options to inject into session storage
    data = AllSettingsSerializer("").data
    data["printers"] = PrinterSerializer(Printer.objects.filter(hidden=False).all(), many=True).data
    data["filaments"] = FilamentSerializer(Filament.objects.filter(hidden=False).all(), many=True).data
    return Response(data)
