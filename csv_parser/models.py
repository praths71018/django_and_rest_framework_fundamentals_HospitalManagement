from django.db import models
from django.contrib.auth.models import User
import csv

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class CSVParser:
    @staticmethod
    def read_csv(file_path):
        data = []
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data

    @staticmethod
    def write_csv(file_path, data):
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
