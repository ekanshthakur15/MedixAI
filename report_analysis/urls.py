from django.urls import path

from .views import *

urlpatterns = [
    path("ai-doctor/", AIDoctorView.as_view()),
    path("symptom-analysis/", SymptomAnalysisView.as_view()),
    path("know-your-medicine/",KnowYourMedicineView.as_view()),
    path("reports/upload/",MedicalReportAnalyseAPIView.as_view()),
    path("reports/list/",MedicalReportListAPIView.as_view()),
    path("reports/list/<int:id>",ReportAttributesListView.as_view()),
    path("report-summary/",ReportSummaryAPIView.as_view()),
    path("reports/attributes/visualisation/<str:element>",MedicalReportAttributeVisualisation.as_view()),
]