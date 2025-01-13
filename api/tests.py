from django.test import TestCase
from django.urls import reverse
from patients.models import Patient
from doctors.models import Doctor
from medicine.models import Medicine
from diseases.models import Disease
from hospitals.models import Hospital  # Import Hospital model
from departments.models import Department  # Import Department model

class PatientStatusViewTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create required related objects first
        self.hospital = Hospital.objects.create(
            Hospital_name="Test Hospital",
            Hospital_address="123 Test St"
        )
        
        self.department = Department.objects.create(
            department_name="Test Department"
        )
        
        self.doctor = Doctor.objects.create(
            doctor_name="Dr. Smith",
            hospital_id=self.hospital,  # Associate with the hospital
            department_id=self.department  # Associate with the department
        )
        
        self.medicine = Medicine.objects.create(medicine_name="Aspirin")  # Create a Medicine instance
        
        self.disease = Disease.objects.create(disease_name="Flu")  # Create a Disease instance
        
        # Create a patient instance for testing
        self.patient_name = "John Doe"
        self.patient = Patient.objects.create(
            patient_name=self.patient_name,
            age=30,
            phone="1234567890",
            doctor=self.doctor,  # Associate with the doctor
            medicine=self.medicine,  # Associate with the medicine
            disease=self.disease,  # Associate with the disease
            status='admitted'
        )

    def test_patient_status_view(self):
        """Test the patient status view"""
        response = self.client.get(reverse('patient-status'), {'name': self.patient_name})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['patient_name'], self.patient_name)

    def test_patient_status_view_patient_not_found(self):
        """Test patient status view when patient is not found"""
        response = self.client.get(reverse('patient-status'), {'name': 'Nonexistent Patient'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], "Patient not found")

    def test_patient_status_view_missing_name(self):
        """Test patient status view when name is missing"""
        response = self.client.get(reverse('patient-status'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Patient name is required")

class PatientVisitHistoryViewTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create required related objects first
        self.hospital = Hospital.objects.create(
            Hospital_name="Test Hospital",
            Hospital_address="123 Test St"
        )
        
        self.department = Department.objects.create(
            department_name="Test Department"
        )
        
        self.doctor = Doctor.objects.create(
            doctor_name="Dr. Smith",
            hospital_id=self.hospital,  # Associate with the hospital
            department_id=self.department  # Associate with the department
        )
        
        self.medicine = Medicine.objects.create(medicine_name="Aspirin")  # Create a Medicine instance
        
        self.disease = Disease.objects.create(disease_name="Flu")  # Create a Disease instance
        
        # Create a patient instance for testing
        self.patient_name = "John Doe"
        self.patient = Patient.objects.create(
            patient_name=self.patient_name,
            age=30,
            phone="1234567890",
            doctor=self.doctor,  # Associate with the doctor
            medicine=self.medicine,  # Associate with the medicine
            disease=self.disease,  # Associate with the disease
            status='admitted'
        )

    def test_patient_visit_history_view(self):
        """Test the patient visit history view"""
        response = self.client.get(reverse('patient-visits'), {'name': self.patient_name})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_patient_visit_history_view_patient_not_found(self):
        """Test patient visit history view when patient is not found"""
        response = self.client.get(reverse('patient-visits'), {'name': 'Nonexistent Patient'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], "No visits found for this patient")

    def test_patient_visit_history_view_missing_name(self):
        """Test patient visit history view when name is missing"""
        response = self.client.get(reverse('patient-visits'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Patient name is required")
