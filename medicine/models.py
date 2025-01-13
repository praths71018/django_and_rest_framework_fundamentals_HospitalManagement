from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

# Create your models here.
class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100)

    def __str__(self):
        return self.medicine_name

# Signals
# receiver is a decorator that allows us to receive signals from the database
# pre_save is a signal that is sent before a model is saved
# sender is the model that is being saved
# instance is the instance of the model that is being saved
# kwargs is a dictionary of keyword arguments
@receiver(pre_save, sender=Medicine)
def send_medicine_notification(sender, instance, **kwargs):
    if instance.medicine_id:  # Check if the medicine already exists (not a new instance)
        previous_instance = sender.objects.get(medicine_id=instance.medicine_id)
        print(f"Medicine updated: {instance.medicine_name}")
        print(f"Previous data: {previous_instance.medicine_name}")
    else:
        print(f"New medicine added: {instance.medicine_name}")

@receiver(pre_delete, sender=Medicine)
def delete_medicine_notification(sender, instance, **kwargs):
    print(f"Medicine deleted: {instance.medicine_name}")

