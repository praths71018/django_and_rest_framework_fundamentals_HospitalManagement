from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Administrator
from hospitals.models import Hospital
from departments.models import Department

class AdministratorTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test hospital
        self.hospital = Hospital.objects.create(
            Hospital_name="Test Hospital",
            Hospital_address="123 Test St"
        )
        
        # Create test departments
        self.dept1 = Department.objects.create(
            department_name="Cardiology"
        )
        self.dept2 = Department.objects.create(
            department_name="Pediatrics"
        )
        
        # Create test administrator with all required fields
        self.admin = Administrator.objects.create(
            admin_name="Test Admin",
            hospital=self.hospital,
            email="testadmin@test.com",
            phone="1234567890"
        )
        self.admin.departments.add(self.dept1, self.dept2)

    def test_get_administrators_list(self):
        """Test getting list of administrators"""
        response = self.client.get(reverse('administrator-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['admin_name'], 'Test Admin')

    def test_create_administrator(self):
        """Test creating a new administrator"""
        data = {
            'admin_name': 'New Admin',
            'hospital': self.hospital.Hospital_id,
            'departments': [self.dept1.department_id, self.dept2.department_id],
            'email': 'newadmin@test.com',
            'phone': '0987654321'
        }
        response = self.client.post(reverse('administrator-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Administrator.objects.count(), 2)
        self.assertEqual(response.data['admin_name'], 'New Admin')
        self.assertEqual(response.data['email'], 'newadmin@test.com')
        self.assertEqual(response.data['phone'], '0987654321')

    def test_get_administrator_detail(self):
        """Test getting administrator detail"""
        response = self.client.get(reverse('administrator-detail', kwargs={'admin_id': self.admin.admin_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['admin_name'], 'Test Admin')
        self.assertEqual(response.data['email'], 'testadmin@test.com')
        self.assertEqual(response.data['phone'], '1234567890')

    def test_update_administrator(self):
        """Test updating administrator"""
        data = {
            'admin_name': 'Updated Admin',
            'hospital': self.hospital.Hospital_id,
            'departments': [self.dept1.department_id],
            'email': 'updated@test.com',
            'phone': '5555555555'
        }
        response = self.client.put(
            reverse('administrator-detail', kwargs={'admin_id': self.admin.admin_id}),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['admin_name'], 'Updated Admin')
        self.assertEqual(response.data['email'], 'updated@test.com')
        self.assertEqual(response.data['phone'], '5555555555')

    def test_delete_administrator(self):
        """Test deleting administrator"""
        response = self.client.delete(reverse('administrator-detail', kwargs={'admin_id': self.admin.admin_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Administrator.objects.count(), 0)

    def test_invalid_hospital_id(self):
        """Test creating administrator with invalid hospital ID"""
        data = {
            'admin_name': 'New Admin',
            'hospital': 999,
            'departments': [self.dept1.department_id],
            'email': 'invalid@test.com',
            'phone': '1231231234'
        }
        response = self.client.post(reverse('administrator-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_department_id(self):
        """Test creating administrator with invalid department ID"""
        data = {
            'admin_name': 'New Admin',
            'hospital': self.hospital.Hospital_id,
            'departments': [999],
            'email': 'invalid@test.com',
            'phone': '1231231234'
        }
        response = self.client.post(reverse('administrator-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        """Test creating administrator with duplicate email"""
        data = {
            'admin_name': 'Another Admin',
            'hospital': self.hospital.Hospital_id,
            'departments': [self.dept1.department_id],
            'email': 'testadmin@test.com',  # Same as existing admin
            'phone': '1231231234'
        }
        response = self.client.post(reverse('administrator-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

