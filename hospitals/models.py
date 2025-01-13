from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

class Hospital(models.Model):
    Hospital_id = models.AutoField(primary_key=True)
    Hospital_name = models.CharField(max_length=100)
    Hospital_address = models.TextField()

    def __str__(self):
        return self.Hospital_name

@receiver(pre_save, sender=Hospital)
def send_hospital_notification(sender, instance, **kwargs):
    if instance.Hospital_id:  # Check if the hospital already exists (not a new instance)
        previous_instance = sender.objects.get(Hospital_id=instance.Hospital_id)
        print(f"Hospital updated: {instance.Hospital_name}")
        print(f"Previous data: {previous_instance.Hospital_name}")
    else:
        print(f"New hospital added: {instance.Hospital_name}")

@receiver(pre_delete, sender=Hospital)
def delete_hospital_notification(sender, instance, **kwargs):
    print(f"Hospital deleted: {instance.Hospital_name}")
