from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Department

class DepartmentTestCase(TestCase):
    def setUp(self):
        Department.objects.create(
            department_name="Cardiology"
        )
        Department.objects.create(
            department_name="Pediatrics"
        )

    def test_department_creation(self):
        cardiology = Department.objects.get(department_name="Cardiology")
        pediatrics = Department.objects.get(department_name="Pediatrics")
        
        self.assertEqual(cardiology.department_name, "Cardiology")
        self.assertEqual(pediatrics.department_name, "Pediatrics")

    def test_department_str(self):
        cardiology = Department.objects.get(department_name="Cardiology")
        self.assertEqual(str(cardiology), "Cardiology")

    def test_department_id_autofield(self):
        cardiology = Department.objects.get(department_name="Cardiology")
        pediatrics = Department.objects.get(department_name="Pediatrics")
        
        self.assertIsNotNone(cardiology.department_id)
        self.assertIsNotNone(pediatrics.department_id)
        self.assertNotEqual(cardiology.department_id, pediatrics.department_id)
