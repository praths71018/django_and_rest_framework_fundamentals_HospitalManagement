from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Hospital

class HospitalTests(APITestCase):
    def setUp(self):
        """Set up test data"""
        # self.hospital is the data to be sent in the POST request.
        self.hospital = Hospital.objects.create(
            Hospital_name="Test Hospital",
            Hospital_address="123 Test St"
        )
        # self.valid_payload is the data to be sent in the POST request.
        self.valid_payload = {
            'Hospital_name': 'New Hospital',
            'Hospital_address': '456 New St'
        }
        # self.invalid_payload is the data to be sent in the POST request.
        self.invalid_payload = {
            'Hospital_name': '',
            'Hospital_address': '456 New St'
        }

    def test_create_valid_hospital(self):
        """Test creating a new hospital with valid data"""
        #  self.client is a test client provided by Django REST framework's APITestCase. It simulates making HTTP requests to your API without actually starting a server.
        response = self.client.post(
            # reverse('hospital-list') is a shortcut function that returns the URL for the hospital-list view (check urls.py).
            reverse('hospital-list'),
            # self.valid_payload is the data to be sent in the POST request.
            self.valid_payload,
            # format='json' is the format of the data to be sent in the POST request.
            format='json'
        )
        # assert that the response status code is 201 i.e. check if response is 201 only or not
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # assert that the hospital count is 2 or not
        self.assertEqual(Hospital.objects.count(), 2)

    def test_create_invalid_hospital(self):
        """Test creating a new hospital with invalid data"""
        response = self.client.post(
            reverse('hospital-list'),
            self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_hospital_list(self):
        """Test retrieving list of hospitals"""
        response = self.client.get(reverse('hospital-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_hospital(self):
        """Test retrieving a single hospital"""
        response = self.client.get(
            reverse('hospital-detail', kwargs={'pk': self.hospital.Hospital_id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Hospital_name'], 'Test Hospital')

    def test_update_hospital(self):
        """Test updating an existing hospital"""
        response = self.client.put(
            reverse('hospital-detail', kwargs={'pk': self.hospital.Hospital_id}),
            self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Hospital_name'], 'New Hospital')

    def test_delete_hospital(self):
        """Test deleting a hospital"""
        response = self.client.delete(
            reverse('hospital-detail', kwargs={'pk': self.hospital.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Hospital.objects.count(), 0)
