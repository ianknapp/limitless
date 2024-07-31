from rest_framework import serializers

from .models import Project, ProjectFile


class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        image = obj.files.filter(file_type=ProjectFile.TypeChoices.IMAGE).first()
        return image.file.url if image else ""

    class Meta:
        model = Project
        fields = ("pk", "title", "image")


class ProjectDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("pk", "title", "description")
