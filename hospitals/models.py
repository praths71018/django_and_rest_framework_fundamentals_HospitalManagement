from django.db import models

class Hospital(models.Model):
    Hospital_id = models.AutoField(primary_key=True)
    Hospital_name = models.CharField(max_length=100)
    Hospital_address = models.TextField()

    def __str__(self):
        return self.Hospital_name
