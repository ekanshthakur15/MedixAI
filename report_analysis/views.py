from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .services import *
from .utils import *


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
    

class MedicalReportAnalyseAPIView(APIView):
    
    def post(self,request, *args, **kwargs):
        file = request.data.get('file')
        if not file:
            return Response({'error':"No file provided"}, status= status.HTTP_400_BAD_REQUEST)
        
        medical_report_data = {
            'user': request.user.id,
            'name': request.data['name'],
            'report': file
        }
        
        medical_report_serializer = MedicalReportSerializer(data = medical_report_data)

        if medical_report_serializer.is_valid():
            medical_report = medical_report_serializer.save()
        else:
            return Response(medical_report_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            files = [
                upload_to_gemini(medical_report.report.path, mime_type="application/pdf")
                ]
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        try:
            user_input = "Strictly return JSON."
            response_text = get_report_analysis(user_input, files=files)
            print(response_text)
            json_object = create_json(response_text)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        # Prepare data for bulk creation
        report_attributes_list = []

        for item in json_object:
            report_attributes_data = {
                'medical_report': medical_report.id,
                'element': item.get('element'),
                'unit': item.get('unit'),
                'reference_low': item.get('reference_low'),
                'reference_high': item.get('reference_high'),
                'result': item.get('results')
            }
            report_attributes_serializer = ReportAttributesSerializer(data=report_attributes_data)
            if report_attributes_serializer.is_valid():
                report_attributes = report_attributes_serializer.save()
                report_attributes_list.append(report_attributes)
            else:
                return Response(report_attributes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        medical_report_response = MedicalReportSerializer(medical_report)
        report_attributes_response = ReportAttributesSerializer(report_attributes_list, many=True)

        return Response({
            'medical_report': medical_report_response.data,
            'report_attributes': report_attributes_response.data
        }, status=status.HTTP_201_CREATED)