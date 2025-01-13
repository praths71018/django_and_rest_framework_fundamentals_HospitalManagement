from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

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

@receiver(pre_save, sender=Doctor)
def send_doctor_notification(sender, instance, **kwargs):
    if instance.doctor_id:  # Check if the doctor already exists (not a new instance)
        previous_instance = sender.objects.get(doctor_id=instance.doctor_id)
        print(f"Doctor updated: {instance.doctor_name}")
        print(f"Previous data: {previous_instance.doctoar_name}")
    else:
        print(f"New doctor added: {instance.doctor_name}")

@receiver(pre_delete, sender=Doctor)
def delete_doctor_notification(sender, instance, **kwargs):
    print(f"Doctor deleted: {instance.doctor_name}")
