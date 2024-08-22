from django.urls import path

from .views import *

urlpatterns = [
    path("ai-doctor/", AIDoctorView.as_view()),
    path("symptom-analysis/", SymptomAnalysisView.as_view()),
    path("know-your-medicine/",KnowYourMedicineView.as_view()),
]