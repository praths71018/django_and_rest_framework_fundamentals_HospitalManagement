from django.test import TestCase
from django.urls import reverse
from .models import Patient
from doctors.models import Doctor
from medicine.models import Medicine
from diseases.models import Disease
from hospitals.models import Hospital
from departments.models import Department

class PatientTestCase(TestCase):
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
            hospital_id=self.hospital,
            department_id=self.department
        )
        
        self.medicine = Medicine.objects.create(medicine_name="Aspirin")
        self.disease = Disease.objects.create(disease_name="Flu")

        # Create test patients
        self.patient = Patient.objects.create(
            patient_name="John Doe",
            age=30,
            phone="1234567890",
            doctor=self.doctor,
            medicine=self.medicine,
            disease=self.disease,
            status='admitted'
        )

    def test_patient_creation(self):
        """Test patient creation and field values"""
        response = self.client.get(reverse('patient-detail', kwargs={'patient_id': self.patient.patient_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['patient_name'], "John Doe")
        self.assertEqual(response.data['age'], 30)
        self.assertEqual(response.data['phone'], "1234567890")
        self.assertEqual(response.data['doctor'], self.doctor.pk)
        self.assertEqual(response.data['medicine'], self.medicine.pk)
        self.assertEqual(response.data['disease'], self.disease.pk)
        self.assertEqual(response.data['status'], 'admitted')

    def test_patient_str(self):
        """Test string representation"""
        self.assertEqual(str(self.patient), "John Doe - admitted")

    def test_patient_id_autofield(self):
        """Test automatic ID generation"""
        self.assertIsNotNone(self.patient.patient_id)

    def test_patient_foreign_key_relationships(self):
        """Test foreign key relationships"""
        self.assertEqual(self.patient.doctor.doctor_name, "Dr. Smith")
        self.assertEqual(self.patient.medicine.medicine_name, "Aspirin")
        self.assertEqual(self.patient.disease.disease_name, "Flu")

    def test_patient_creation_invalid_foreign_key(self):
        """Test patient creation with invalid foreign key"""
        response = self.client.post(reverse('patient-list'), {
            'patient_name': 'Jane Doe',
            'age': 25,
            'phone': '0987654321',
            'doctor': 999,  # Invalid doctor ID
            'medicine': self.medicine.pk,
            'disease': self.disease.pk,
            'status': 'admitted'
        })
        self.assertEqual(response.status_code, 400)

    def test_patient_update(self):
        """Test updating an existing patient"""
        response = self.client.put(
            reverse('patient-detail', kwargs={'patient_id': self.patient.patient_id}),
            {
                'patient_name': 'John Updated',
                'age': 31,
                'phone': '1234567890',
                'doctor': self.doctor.pk,
                'medicine': self.medicine.pk,
                'disease': self.disease.pk,
                'status': 'discharged'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.patient_name, 'John Updated')
        self.assertEqual(self.patient.status, 'discharged')

    def test_patient_delete(self):
        """Test deleting a patient"""
        response = self.client.delete(reverse('patient-detail', kwargs={'patient_id': self.patient.patient_id}))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Patient.objects.filter(patient_id=self.patient.patient_id).exists())

