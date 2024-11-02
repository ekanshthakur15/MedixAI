from rest_framework import serializers

from .models import *


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = "__all__"
class MedicalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalReport
        fields = "__all__"

class ReportAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportAttributes
        fields = "__all__"

class ReportSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSummary
        fields = "__all__"
