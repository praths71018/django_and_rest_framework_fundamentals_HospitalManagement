from django.db import models
from hospitals.models import Hospital
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

# Create your models here.
class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name

@receiver(pre_save, sender=Department)
def send_department_notification(sender, instance, **kwargs):
    if instance.department_id:  # Check if the department already exists (not a new instance)
        previous_instance = sender.objects.get(department_id=instance.department_id)
        print(f"Department updated: {instance.department_name}")
        print(f"Previous data: {previous_instance.department_name}")
    else:
        print(f"New department added: {instance.department_name}")

@receiver(pre_delete, sender=Department)
def delete_department_notification(sender, instance, **kwargs):
    print(f"Department deleted: {instance.department_name}")
