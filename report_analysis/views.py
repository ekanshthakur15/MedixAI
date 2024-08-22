from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .services import *


# API View for AI Doctor
class AIDoctorView(APIView):

    def post(self, request):
        user_input = request.data.get('query')
        if not user_input:
            return Response({"error": "Message content is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = ai_doctor(user_input)
        
        return Response({"response": response}, status=status.HTTP_200_OK)
    
# API View for Symptom Analysis
class SymptomAnalysisView(APIView):

    def post(self, request):
        user_input = request.data.get('query')
        if not user_input:
            return Response({"error": "Message content is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = get_symptom_analysis(user_input)

        return Response({"response": response}, status=status.HTTP_200_OK)
    
# API View for Know Your Medicine
class KnowYourMedicineView(APIView):

    def post(self, request):
        user_input = request.data.get('query')
        if not user_input:
            return Response({"error": "Message content is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = know_your_medicine(user_input)

        return Response({"response": response}, status=status.HTTP_200_OK)