from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("pk", "title")


class ProjectDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "description")
