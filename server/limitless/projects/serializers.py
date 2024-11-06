from rest_framework import serializers

from limitless.cura.serializers import CuraSettingsSerializer

from .models import Filament, Printer, Project, ProjectFile, UserProfile


class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        image = obj.files.filter(file_type=ProjectFile.TypeChoices.IMAGE, primary=True).first()
        return image.file.url if image else ""

    class Meta:
        model = Project
        fields = ("id", "title", "image", "recently_viewed")


class ProjectCreationSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        data["owner"] = self.context["owner"]
        return super().to_internal_value(data)

    class Meta:
        model = Project
        fields = ("title", "description", "owner")


class ProjectDetailsSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    secondary_image = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    settings = CuraSettingsSerializer(required=False)

    def get_primary_image(self, obj):
        image = obj.files.filter(file_type=ProjectFile.TypeChoices.IMAGE, primary=True).first()
        return image.file.url if image else ""

    def get_secondary_image(self, obj):
        image = obj.files.filter(file_type=ProjectFile.TypeChoices.IMAGE, primary=False).first()
        return image.file.url if image else ""

    def get_model(self, obj):
        model = obj.files.filter(file_type=ProjectFile.TypeChoices.MODEL, primary=False).first()
        return model.file.url if model else ""

    class Meta:
        model = Project
        fields = ("id", "title", "description", "primary_image", "secondary_image", "model", "settings")
        read_only = ["settings"]


class PrinterSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="name")
    value = serializers.CharField(source="id")

    class Meta:
        model = Printer
        fields = ("label", "value")


class FilamentSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="name")
    value = serializers.CharField(source="id")

    class Meta:
        model = Filament
        fields = ("label", "value")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("minimize_supports", "printer", "filament")
