from rest_framework import serializers

from .models import CuraSettings
from .settings import AdhesionType, SupportStructure, SupportType


class AllSettingsSerializer(serializers.Serializer):
    support_structures = serializers.SerializerMethodField()
    support_types = serializers.SerializerMethodField()
    adhesion_types = serializers.SerializerMethodField()

    def get_support_structures(self, obj):
        return [{"value": value, "label": label} for value, label in SupportStructure.choices]

    def get_support_types(self, obj):
        return [{"value": value, "label": label} for value, label in SupportType.choices]

    def get_adhesion_types(self, obj):
        return [{"value": value, "label": label} for value, label in AdhesionType.choices]

    class Meta:
        fields = ["support_structures", "support_types", "adhesion_types"]


class CuraSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuraSettings
        fields = ("enable_support", "support_type", "support_structure", "infill_sparse_density", "adhesion_type")
