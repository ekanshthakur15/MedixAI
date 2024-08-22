from rest_framework import serializers

from .models import *


class MedicalReportSerializer(serializers.Serializer):
    class Meta:
        model = MedicalReport
        fields = "__all__"

class ReportAttributesSerializer(serializers.Serializer):
    class Meta:
        model = ReportAttributes
        fields = "__all__"

class ReportSummarySerializer(serializers.Serializer):
    class Meta:
        model = ReportSummary
        fields = "__all__"
