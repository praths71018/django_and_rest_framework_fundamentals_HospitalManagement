from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from patients.models import Patient
from .serializers import PatientStatusSerializer, PatientVisitHistorySerializer
from django.db.models import Q
from datetime import datetime

class PatientStatusView(APIView):
    def get(self, request):
        patient_name = request.query_params.get('name')
        if not patient_name:
            return Response(
                {"error": "Patient name is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get the most recent visit for the patient
            patient = Patient.objects.filter(
                patient_name__iexact=patient_name
            ).order_by('-visit_time').first()
            
            if not patient:
                return Response(
                    {"error": "Patient not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = PatientStatusSerializer(patient)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PatientVisitHistoryView(APIView):
    def get(self, request):
        patient_name = request.query_params.get('name')

        if not patient_name:
            return Response(
                {"error": "Patient name is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Base query
            query = Q(patient_name__iexact=patient_name)
            # Get all visits ordered by date
            visits = Patient.objects.filter(query).order_by('-visit_time')

            if not visits:
                return Response(
                    {"error": "No visits found for this patient"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = PatientVisitHistorySerializer(visits, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
