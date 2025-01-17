from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer, PatientStatusSerializer, PatientVisitHistorySerializer
from doctors.models import Doctor
from medicine.models import Medicine 
from diseases.models import Disease
from django.db.models import Q
from datetime import datetime
from .tasks import send_patient_email  # Import the task to send email

class PatientListView(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        # Decrypt phone numbers for each patient
        for patient in patients:
            patient.phone = patient.get_decrypted_phone()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Validate foreign keys exist
        try:
            doctor = Doctor.objects.get(pk=data.get('doctor'))
            medicine = Medicine.objects.get(pk=data.get('medicine'))
            disease = Disease.objects.get(pk=data.get('disease'))
        except (Doctor.DoesNotExist, Medicine.DoesNotExist, Disease.DoesNotExist) as e:
            return Response(
                {"error": "Referenced foreign key does not exist"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PatientSerializer(data=data)
        if serializer.is_valid():
            patient = serializer.save()  # Save the patient instance
            # Send email asynchronously using celery
            send_patient_email.delay(patient.patient_id)  # Send email asynchronously
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientDetailView(APIView):
    def get_object(self, patient_id):
        try:
            return Patient.objects.get(patient_id=patient_id)
        except Patient.DoesNotExist:
            return None

    def get(self, request, patient_id):
        patient = self.get_object(patient_id)
        if not patient:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Decrypt phone number for the patient
        patient.phone = patient.get_decrypted_phone()
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def put(self, request, patient_id):
        patient = self.get_object(patient_id)
        if not patient:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        
        # Validate foreign keys if they are being updated
        if 'doctor' in data:
            try:
                doctor = Doctor.objects.get(pk=data.get('doctor'))
            except Doctor.DoesNotExist:
                return Response(
                    {"error": "Referenced doctor does not exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        if 'medicine' in data:
            try:
                medicine = Medicine.objects.get(pk=data.get('medicine'))
            except Medicine.DoesNotExist:
                return Response(
                    {"error": "Referenced medicine does not exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        if 'disease' in data:
            try:
                disease = Disease.objects.get(pk=data.get('disease'))
            except Disease.DoesNotExist:
                return Response(
                    {"error": "Referenced disease does not exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = PatientSerializer(patient, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, patient_id):
        patient = self.get_object(patient_id)
        if not patient:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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
            
            # Decrypt phone number for the patient
            patient.phone = patient.get_decrypted_phone()
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

            # Decrypt phone numbers for each visit
            for visit in visits:
                visit.phone = visit.get_decrypted_phone()

            serializer = PatientVisitHistorySerializer(visits, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Patient
# from .serializers import PatientSerializer
# from doctors.models import Doctor
# from medicine.models import Medicine 
# from diseases.models import Disease

# @api_view(['GET', 'POST'])
# def patient_list(request):
#     if request.method == 'GET':
#         patients = Patient.objects.all()
#         serializer = PatientSerializer(patients, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         data = request.data
        
#         # Validate foreign keys exist
#         try:
#             doctor = Doctor.objects.get(pk=data.get('doctor'))
#             medicine = Medicine.objects.get(pk=data.get('medicine'))
#             disease = Disease.objects.get(pk=data.get('disease'))
#         except (Doctor.DoesNotExist, Medicine.DoesNotExist, Disease.DoesNotExist) as e:
#             return Response(
#                 {"error": "Referenced foreign key does not exist"}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = PatientSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def patient_detail(request, patient_id):
#     try:
#         patient = Patient.objects.get(patient_id=patient_id)
#     except Patient.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = PatientSerializer(patient)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         data = request.data
        
#         # Validate foreign keys if they are being updated
#         if 'doctor' in data:
#             try:
#                 doctor = Doctor.objects.get(pk=data.get('doctor'))
#             except Doctor.DoesNotExist:
#                 return Response(
#                     {"error": "Referenced doctor does not exist"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
                
#         if 'medicine' in data:
#             try:
#                 medicine = Medicine.objects.get(pk=data.get('medicine'))
#             except Medicine.DoesNotExist:
#                 return Response(
#                     {"error": "Referenced medicine does not exist"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
                
#         if 'disease' in data:
#             try:
#                 disease = Disease.objects.get(pk=data.get('disease'))
#             except Disease.DoesNotExist:
#                 return Response(
#                     {"error": "Referenced disease does not exist"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#         serializer = PatientSerializer(patient, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         patient.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
