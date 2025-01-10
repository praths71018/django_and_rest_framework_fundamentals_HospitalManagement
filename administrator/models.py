from django.db import models
from hospitals.models import Hospital
from departments.models import Department

class Administrator(models.Model):
    admin_id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='administrators')
    departments = models.ManyToManyField(Department, related_name='administrators')
    admin_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin_name} - {self.hospital.Hospital_name}"
