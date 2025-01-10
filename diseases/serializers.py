from rest_framework import serializers
from .models import Disease

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ['disease_id', 'disease_name']
        read_only_fields = ['disease_id']
