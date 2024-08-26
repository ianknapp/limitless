from rest_framework import serializers

from .settings import AdhesionType, SupportStruture, SupportType


class SettingsSerializer(serializers.Serializer):
    support_structures = serializers.SerializerMethodField()
    support_types = serializers.SerializerMethodField()
    adhesion_types = serializers.SerializerMethodField()

    def get_support_structures(self, obj):
        return [{"value": value, "label": label} for value, label in SupportStruture.choices]

    def get_support_types(self, obj):
        return [{"value": value, "label": label} for value, label in SupportType.choices]

    def get_adhesion_types(self, obj):
        return [{"value": value, "label": label} for value, label in AdhesionType.choices]

    class Meta:
        fields = ["support_structures", "support_types", "adhesion_types"]
