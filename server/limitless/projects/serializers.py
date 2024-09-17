from rest_framework import serializers

from limitless.cura.serializers import CuraSettingsSerializer

from .models import Printer, Project, ProjectFile, UserProfile


class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        image = obj.files.filter(file_type=ProjectFile.TypeChoices.IMAGE, primary=True).first()
        return image.file.url if image else ""

    class Meta:
        model = Project
        fields = ("id", "title", "image")


class ProjectDetailsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    settings = CuraSettingsSerializer(required=False)

    def get_image(self, obj):
        image = obj.files.filter(file_type=ProjectFile.TypeChoices.IMAGE, primary=False).first()
        return image.file.url if image else ""

    def get_model(self, obj):
        model = obj.files.filter(file_type=ProjectFile.TypeChoices.MODEL, primary=False).first()
        return model.file.url if model else ""

    class Meta:
        model = Project
        fields = ("id", "title", "description", "image", "model", "settings")
        read_only = ["settings"]


class PrinterSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="name")
    value = serializers.CharField(source="id")

    class Meta:
        model = Printer
        fields = ("label", "value")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("minimize_supports", "printer")
