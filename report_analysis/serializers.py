from urllib.parse import urljoin

from django.conf import settings
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Construct the full URL for the report
        if representation['report']:
            representation['report'] = urljoin(
                settings.BASE_URL, representation['report'])

        return representation


class ReportAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportAttributes
        fields = "__all__"


class ReportSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSummary
        fields = "__all__"

# Store user's keywords for search indexing


class UserKeyword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.keyword}"
