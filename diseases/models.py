from django.db import models

# Create your models here.
class Disease(models.Model):
    disease_id = models.AutoField(primary_key=True)
    disease_name = models.CharField(max_length=100)

    def __str__(self):
        return self.disease_name
