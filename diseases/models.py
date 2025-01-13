from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

# Create your models here.
class Disease(models.Model):
    disease_id = models.AutoField(primary_key=True)
    disease_name = models.CharField(max_length=100)

    def __str__(self):
        return self.disease_name


@receiver(pre_save, sender=Disease)
def send_disease_notification(sender, instance, **kwargs):
    if instance.disease_id:  # Check if the disease already exists (not a new instance)
        previous_instance = sender.objects.get(disease_id=instance.disease_id)
        print(f"Disease updated: {instance.disease_name}")
        print(f"Previous data: {previous_instance.disease_name}")
    else:
        print(f"New disease added: {instance.disease_name}")

@receiver(pre_delete, sender=Disease)
def delete_disease_notification(sender, instance, **kwargs):
    print(f"Disease deleted: {instance.disease_name}")
