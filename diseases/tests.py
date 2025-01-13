from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Disease

class DiseaseTestCase(TestCase):
    def setUp(self):
        Disease.objects.create(
            disease_name="Fever"
        )
        Disease.objects.create(
            disease_name="Flu"
        )

    def test_disease_creation(self):
        fever = Disease.objects.get(disease_name="Fever")
        flu = Disease.objects.get(disease_name="Flu")
        
        self.assertEqual(fever.disease_name, "Fever")
        self.assertEqual(flu.disease_name, "Flu")

    def test_disease_str(self):
        fever = Disease.objects.get(disease_name="Fever")
        self.assertEqual(str(fever), "Fever")

    def test_disease_id_autofield(self):
        fever = Disease.objects.get(disease_name="Fever")
        flu = Disease.objects.get(disease_name="Flu")
        
        self.assertIsNotNone(fever.disease_id)
        self.assertIsNotNone(flu.disease_id)
        self.assertNotEqual(fever.disease_id, flu.disease_id)
