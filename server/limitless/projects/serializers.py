from rest_framework import serializers

from .models import Printer, Project, ProjectFile


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

    def get_image(self, obj):
        image = obj.files.filter(file_type=ProjectFile.TypeChoices.IMAGE, primary=False).first()
        return image.file.url if image else ""

    class Meta:
        model = Project
        fields = ("id", "title", "description", "image")


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ("id", "name")
