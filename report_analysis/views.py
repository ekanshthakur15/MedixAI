import math
import os
from datetime import date  # Correct import

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .recommendation_utils import *
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


class TreatmentListAPIView(APIView):
    def post(self, request):
        user = request.user
        request.data['user'] = user.id
        serializer = TreatmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Treatment was created successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        treatments = Treatment.objects.filter(user=user)
        serializer = TreatmentSerializer(treatments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MedicalReportListAPIView(APIView):

    def get(self, request):

        user = request.user

        medical_reports = MedicalReport.objects.filter(user=user)

        serializers = MedicalReportSerializer(medical_reports, many=True)

        return Response({'medical_reports': serializers.data}, status=status.HTTP_200_OK)


class MedicalReportsByTreatmentAPIView(APIView):

    def get(self, request, treatment_name):

        user = request.user
        try:
            treatment = Treatment.objects.get(name=treatment_name, user=user)
        except Treatment.DoesNotExist:
            return Response({"error": "Treatment doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        medical_reports = MedicalReport.objects.filter(
            user=user, treatment=treatment)

        serializers = MedicalReportSerializer(medical_reports, many=True)

        return Response({'medical_reports': serializers.data}, status=status.HTTP_200_OK)


class AttributesListByTreatment(APIView):
    def get(self, request):
        user = request.user
        # try:
        #     treatment = Treatment.objects.get(name = treatment_name, user = user)
        # except Treatment.DoesNotExist:
        #     return Response({"error":"Treatment doesn't exist"}, status= status.HTTP_404_NOT_FOUND)

        # Step 4: Get all ReportAttributes associated with this treatment
        # This is done by filtering through the MedicalReport and then ReportAttributes
        report_attributes = ReportAttributes.objects.filter(
            medical_report__user=user)

        # Step 5: Extract unique 'element' values
        unique_elements = report_attributes.values_list(
            'element', flat=True).distinct()

        # Step 6: Return the unique elements in the response
        return Response({"attributes": list(unique_elements)}, status=status.HTTP_200_OK)


class ReportAttributesListView(APIView):

    def get(self, request, id):

        try:
            medical_report = MedicalReport.objects.get(id=id)
        except MedicalReport.DoesNotExist:
            return Response({"error": "Medical Report not found"}, status=status.HTTP_404_NOT_FOUND)

        attributes = ReportAttributes.objects.filter(
            medical_report=medical_report)

        serializer = ReportAttributesSerializer(attributes, many=True)

        return Response({"attributes": serializer.data}, status=status.HTTP_200_OK)


class MedicalReportAPIView(APIView):

    def post(self, request, *args, **kwargs):
        file = request.data.get('file')
        if not file:
            return Response({'error': "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        medical_report_data = {
            'user': request.user.id,
            'name': request.data['name'],
            'report': file
        }

        treatment_name = request.data.get('treatment')
        print(treatment_name)

        if treatment_name:
            treatment = Treatment.objects.get(
                user=request.user, name=treatment_name)
            medical_report_data['treatment'] = treatment.id

        medical_report_serializer = MedicalReportSerializer(
            data=medical_report_data)

        if medical_report_serializer.is_valid():
            medical_report = medical_report_serializer.save()
        else:
            return Response(medical_report_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            files = [upload_to_gemini(
                medical_report.report.path, mime_type="application/pdf")]
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            user_input = "Strictly return JSON."
            response_text = get_report_analysis(user_input, files=files)
            json_object = create_json(response_text)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Attempt to create a summary for the report
        try:
            summary_prompt = "Create a detailed summary of the report with the possible and potential health issues"
            response_summary = get_report_analysis(summary_prompt, files=files)
            if not response_summary:
                return Response({'error': "Summary generation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Prepare the summary data
            summary_data = {
                "medical_report": medical_report.id,
                "summary": response_summary
            }

            # Validate and save the summary
            serializer = ReportSummarySerializer(data=summary_data)
            if serializer.is_valid():
                serializer.save()
                print("Summary created successfully")
            else:
                print("Summary serializer errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Prepare data for bulk creation of attributes
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
            report_attributes_serializer = ReportAttributesSerializer(
                data=report_attributes_data)
            if report_attributes_serializer.is_valid():
                report_attributes = report_attributes_serializer.save()
                report_attributes_list.append(report_attributes)
            else:
                return Response(report_attributes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        medical_report_response = MedicalReportSerializer(medical_report)
        report_attributes_response = ReportAttributesSerializer(
            report_attributes_list, many=True)

        return Response({
            'medical_report': medical_report_response.data,
            'report_attributes': report_attributes_response.data
        }, status=status.HTTP_201_CREATED)


class MedicalReportDetailAPIView(APIView):
    def get(self, request, report_id):

        try:
            report = MedicalReport.objects.get(user=request.user, id=report_id)
            medical_report = MedicalReportSerializer(report)
        except MedicalReport.DoesNotExist:
            return Response({"error": "Medical Report does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            query_set = ReportAttributes.objects.filter(medical_report=report)
            attributes_data = []
            for attribute in query_set:
                # Set defaults for low and high values
                try:
                    low = float(attribute.reference_low) if attribute.reference_low not in [
                        None, ""] else 0
                    high = float(attribute.reference_high) if attribute.reference_high not in [
                        None, ""] else math.inf
                    result = float(attribute.result)
                    # Determine condition
                    condition = getCondition(result, low, high)
                except ValueError:
                    # Handle invalid conversions
                    condition = "undefined"

                attribute_data = ReportAttributesSerializer(attribute).data
                attribute_data["condition"] = condition
                attributes_data.append(attribute_data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            summary = ReportSummary.objects.get(medical_report=report)
            summary_serializer = ReportSummarySerializer(summary)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {
            "medical_report": medical_report.data,
            "attributes": attributes_data,
            "summary": summary_serializer.data["summary"]
        }
        return Response(data, status=status.HTTP_200_OK)


# API to create Report Summary
class ReportSummaryAPIView(APIView):

    def post(self, request):

        file = request.data.get('file')

        if not file:
            return Response({"error": "file is required"}, status=status.HTTP_400_BAD_REQUEST)

        file_path = save_temp_file(file)

        try:
            files = [
                upload_to_gemini(file_path, mime_type="application/pdf")
            ]
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            user_input = "Create a detailed summary of the report."
            response_text = get_report_analysis(user_input, files=files)
            print(response_text)
            if os.path.exists(file_path):
                os.remove(file_path)
            return Response({"response": response_text}, status=status.HTTP_200_OK)

        except Exception as e:

            if os.path.exists(file_path):
                os.remove(file_path)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MedicalReportAttributeVisualisation(APIView):

    def get(self, request, element):
        # Initialize the lists for dates and attributes
        dates = []
        attributes = []

        # Get startDate and endDate from query params, if provided
        start_date_str = request.query_params.get('startDate', None)
        end_date_str = request.query_params.get('endDate', None)

        # Parse the dates if they are provided
        if start_date_str:
            try:
                start_date = date.fromisoformat(
                    start_date_str)  # Converts string to date
            except ValueError:
                return Response({"error": "Invalid startDate format. Use 'YYYY-MM-DD'."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = date.fromisoformat(
                    end_date_str)  # Converts string to date
            except ValueError:
                return Response({"error": "Invalid endDate format. Use 'YYYY-MM-DD'."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            end_date = None

        # Filter medical reports based on the user
        medical_reports = MedicalReport.objects.filter(user=request.user)

        # Apply date filters if both start_date and end_date are provided
        if start_date:
            medical_reports = medical_reports.filter(test_date__gte=start_date)
        if end_date:
            medical_reports = medical_reports.filter(test_date__lte=end_date)

        for medical_report in medical_reports:
            # Find the first attribute matching the element in the medical report
            attribute = ReportAttributes.objects.filter(
                medical_report=medical_report, element=element).first()

            if attribute:
                # If the attribute exists, add the date and attribute to the lists
                dates.append(medical_report.test_date)
                attributes.append({
                    'element': attribute.element,
                    'unit': attribute.unit,
                    'reference_low': float(attribute.reference_low) if attribute.reference_low else float('-inf'),
                    'reference_high': float(attribute.reference_high) if attribute.reference_high else float('inf'),
                    'result': float(attribute.result) if attribute.result else None
                })
            else:
                print(
                    f"Attribute not present for {medical_report.name} on {medical_report.test_date}")

        # Return the dates and attributes as separate arrays in the response
        return Response({
            'dates': dates,
            'attributes': attributes
        }, status=status.HTTP_200_OK)


class ArticleSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)
        if not query:
            return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Search Elasticsearch for matching articles
        articles = search_articles(query)

        if not articles:
            return Response({"message": "No articles found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(articles, status=status.HTTP_200_OK)


class ArticleRecommendationAPIView(APIView):
    """
    API View to recommend articles based on the user's medical report summaries.
    The user is identified through `request.user` (authenticated user).
    This API uses GET method.
    """

    def get(self, request, *args, **kwargs):
        # Extract user from request.user (assuming the user is authenticated)
        user = request.user

        # if not user.is_authenticated:
        #     return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        # Fetch the report summaries for the authenticated user
        report_summaries = []
        medical_reports = MedicalReport.objects.filter(user=user)

        if not medical_reports:
            return Response({"error": "No reports found for the authenticated user."}, status=status.HTTP_404_NOT_FOUND)

        # Get summaries from ReportSummary model
        for report in medical_reports:
            summary = ReportSummary.objects.filter(
                medical_report=report).first()
            if summary and summary.summary:
                report_summaries.append(summary.summary)

        # Check if there are any summaries to generate a query
        if not report_summaries:
            return Response({"error": "No summaries found for the given reports."}, status=status.HTTP_404_NOT_FOUND)

        # Generate a query based on the concatenated summaries
        query = generate_query_from_summary(report_summaries)

        print(query)

        if not query:
            return Response({"error": "Failed to generate a query from the report summaries."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Use the generated query to search for relevant articles in Elasticsearch
        articles = search_articles(query)

        if not articles:
            return Response({"message": "No articles found matching the query."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"articles": articles}, status=status.HTTP_200_OK)
