from rest_framework import serializers
from .models import Hospital

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['Hospital_id', 'Hospital_name', 'Hospital_address'] 