from django.db import models

# Create your models here.
class Doctor(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    
    doctor_id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=100)
    hospital_id = models.ForeignKey('hospitals.Hospital', on_delete=models.CASCADE)
    department_id = models.ForeignKey('departments.Department', on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.doctor_name
