from django.db import models
from doctors.models import Doctor
from medicine.models import Medicine
from diseases.models import Disease

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

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
    email = models.EmailField(max_length=254,default='shetty123@gmail.com')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    visit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.status}"

@receiver(pre_save, sender=Patient)
def send_patient_notification(sender, instance, **kwargs):
    if instance.patient_id:  # Check if the patient already exists (not a new instance)
        previous_instance = sender.objects.get(patient_id=instance.patient_id)
        print(f"Patient updated: {instance.patient_name}")
        print(f"Previous data: {previous_instance.patient_name}, Status: {previous_instance.status}")
    else:
        print(f"New patient added: {instance.patient_name}")

@receiver(pre_delete, sender=Patient)
def delete_patient_notification(sender, instance, **kwargs):
    print(f"Patient deleted: {instance.patient_name}")
