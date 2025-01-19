from rest_framework import serializers
from .models import Patient
from doctors.models import Doctor
from hospitals.models import Hospital
from departments.models import Department

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_id', 'patient_name', 'age', 'phone','email', 'doctor', 'medicine', 'disease', 'status', 'visit_time']


class DoctorSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital_id.Hospital_name', read_only=True)
    department_name = serializers.CharField(source='department_id.department_name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['doctor_id', 'doctor_name', 'hospital_name', 'department_name', 'status']

class PatientStatusSerializer(serializers.ModelSerializer):
    doctor_details = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = Patient
        fields = [
            'patient_id',
            'patient_name',
            'status',
            'visit_time',
            'doctor_details'
        ]

class PatientVisitHistorySerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.doctor_name', read_only=True)
    hospital_name = serializers.CharField(source='doctor.hospital_id.Hospital_name', read_only=True)
    department_name = serializers.CharField(source='doctor.department_id.department_name', read_only=True)

    class Meta:
        model = Patient
        fields = [
            'patient_id',
            'patient_name',
            'visit_time',
            'status',
            'doctor_name',
            'hospital_name',
            'department_name'
        ] 