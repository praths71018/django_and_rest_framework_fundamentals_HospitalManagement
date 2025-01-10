from django.db import models
from doctors.models import Doctor
from medicine.models import Medicine
from diseases.models import Disease

# Create your models here.
class Patient(models.Model):
    STATUS_CHOICES = [
        ('discharged', 'Discharged'),
        ('admitted', 'Admitted'),
        ('waiting', 'Waiting')
    ]

    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=15)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    visit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.status}"

