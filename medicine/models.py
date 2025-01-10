from django.db import models

# Create your models here.
class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100)

    def __str__(self):
        return self.medicine_name
