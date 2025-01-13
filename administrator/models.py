from django.db import models
from hospitals.models import Hospital
from departments.models import Department
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

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

@receiver(pre_save, sender=Administrator)
def send_administrator_notification(sender, instance, **kwargs):
    if instance.admin_id:  # Check if the administrator already exists (not a new instance)
        previous_instance = sender.objects.get(admin_id=instance.admin_id)
        print(f"Administrator updated: {instance.admin_name}")
        print(f"Previous data: {previous_instance.admin_name}, Hospital: {previous_instance.hospital.Hospital_name}")
    else:
        print(f"New administrator added: {instance.admin_name}")

@receiver(pre_delete, sender=Administrator)
def delete_administrator_notification(sender, instance, **kwargs):
    print(f"Administrator deleted: {instance.admin_name}")
