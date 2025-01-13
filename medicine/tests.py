from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Medicine

class MedicineTestCase(TestCase):
    def setUp(self):
        Medicine.objects.create(
            medicine_name="Paracetamol"
        )
        Medicine.objects.create(
            medicine_name="Amoxicillin"
        )

    def test_medicine_creation(self):
        paracetamol = Medicine.objects.get(medicine_name="Paracetamol")
        amoxicillin = Medicine.objects.get(medicine_name="Amoxicillin")
        
        self.assertEqual(paracetamol.medicine_name, "Paracetamol")
        self.assertEqual(amoxicillin.medicine_name, "Amoxicillin")

    def test_medicine_str(self):
        paracetamol = Medicine.objects.get(medicine_name="Paracetamol")
        self.assertEqual(str(paracetamol), "Paracetamol")

    def test_medicine_id_autofield(self):
        paracetamol = Medicine.objects.get(medicine_name="Paracetamol")
        amoxicillin = Medicine.objects.get(medicine_name="Amoxicillin")
        
        self.assertIsNotNone(paracetamol.medicine_id)
        self.assertIsNotNone(amoxicillin.medicine_id)
        self.assertNotEqual(paracetamol.medicine_id, amoxicillin.medicine_id)

