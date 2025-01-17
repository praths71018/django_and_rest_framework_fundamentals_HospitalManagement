from django.db import models
from doctors.models import Doctor
from medicine.models import Medicine
from diseases.models import Disease

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

import logging
import os

from .utils.encryption import encrypt, decrypt  # Import the encrypt and decrypt functions

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
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=254,default='shetty123@gmail.com')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    visit_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Encrypt the phone number before saving
        if self.phone:
            self.phone = encrypt(self.phone)
        super().save(*args, **kwargs)

    def get_decrypted_phone(self):
        # Decrypt the phone number when retrieving
        return decrypt(self.phone) if self.phone else None # Return None if decryption fails

    def __str__(self):
        return f"{self.patient_name} - {self.status}"
    
# Set up audit log configuration
audit_log_file_path = os.path.join('logs', 'audit.log')  # Ensure the 'logs' directory exists
os.makedirs(os.path.dirname(audit_log_file_path), exist_ok=True)

audit_logger = logging.getLogger('audit_logger')
audit_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(audit_log_file_path)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
audit_logger.addHandler(file_handler)

@receiver(pre_save, sender=Patient)
def send_patient_notification(sender, instance, **kwargs):
    if instance.patient_id:  # Check if the patient already exists (not a new instance)
        previous_instance = sender.objects.get(patient_id=instance.patient_id)
        message_update = f"Patient updated: {instance.patient_name}"
        message_previous = f"Previous data: {previous_instance.patient_name}, Status: {previous_instance.status}"
        print(message_update)
        print(message_previous)
        audit_logger.info(message_update)
        audit_logger.info(message_previous)
    else:
        message_new = f"New patient added: {instance.patient_name}"
        print(message_new)
        audit_logger.info(message_new)

@receiver(pre_delete, sender=Patient)
def delete_patient_notification(sender, instance, **kwargs):
    message_delete = f"Patient deleted: {instance.patient_name}"
    print(message_delete)
    audit_logger.info(message_delete)
