from django.test import TestCase
from .models import Doctor
from hospitals.models import Hospital
from departments.models import Department

class DoctorTestCase(TestCase):
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
        
        # Create test doctors
        self.smith = Doctor.objects.create(
            doctor_name="Dr. Smith",
            hospital_id=self.hospital,
            department_id=self.department,
            status='active'
        )
        
        self.jones = Doctor.objects.create(
            doctor_name="Dr. Jones",
            hospital_id=self.hospital,
            department_id=self.department,
            status='inactive'
        )

    def test_doctor_creation(self):
        """Test doctor creation and field values"""
        smith = Doctor.objects.get(doctor_name="Dr. Smith")
        jones = Doctor.objects.get(doctor_name="Dr. Jones")
        
        self.assertEqual(smith.doctor_name, "Dr. Smith")
        self.assertEqual(jones.doctor_name, "Dr. Jones")
        self.assertEqual(smith.status, "active")
        self.assertEqual(jones.status, "inactive")
        self.assertEqual(smith.hospital_id, self.hospital)
        self.assertEqual(smith.department_id, self.department)

    def test_doctor_str(self):
        """Test string representation"""
        smith = Doctor.objects.get(doctor_name="Dr. Smith")
        self.assertEqual(str(smith), "Dr. Smith")

    def test_doctor_id_autofield(self):
        """Test automatic ID generation"""
        smith = Doctor.objects.get(doctor_name="Dr. Smith")
        jones = Doctor.objects.get(doctor_name="Dr. Jones")
        
        self.assertIsNotNone(smith.doctor_id)
        self.assertIsNotNone(jones.doctor_id)
        self.assertNotEqual(smith.doctor_id, jones.doctor_id)

    def test_doctor_status_choices(self):
        """Test status field choices"""
        smith = Doctor.objects.get(doctor_name="Dr. Smith")
        self.assertIn(smith.status, dict(Doctor.STATUS_CHOICES))

    def test_foreign_key_relationships(self):
        """Test foreign key relationships"""
        smith = Doctor.objects.get(doctor_name="Dr. Smith")
        self.assertEqual(smith.hospital_id.Hospital_name, "Test Hospital")
        self.assertEqual(smith.department_id.department_name, "Test Department")
