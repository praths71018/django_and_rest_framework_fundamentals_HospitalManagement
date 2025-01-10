from rest_framework import serializers
from .models import Administrator
from hospitals.serializers import HospitalSerializer
from departments.serializers import DepartmentSerializer
from hospitals.models import Hospital
from departments.models import Department

class AdministratorSerializer(serializers.ModelSerializer):
    hospital_details = HospitalSerializer(source='hospital', read_only=True)
    department_details = DepartmentSerializer(source='departments', many=True, read_only=True)
    
    hospital = serializers.PrimaryKeyRelatedField(queryset=Hospital.objects.all())
    departments = serializers.PrimaryKeyRelatedField(many=True, queryset=Department.objects.all())

    class Meta:
        model = Administrator
        fields = [
            'admin_id', 
            'hospital', 
            'hospital_details',
            'departments',
            'department_details',
            'admin_name', 
            'email', 
            'phone', 
            'date_joined'
        ]
        read_only_fields = ['admin_id', 'date_joined', 'hospital_details', 'department_details']

    def create(self, validated_data):
        # Extract departments from validated data
        departments_data = validated_data.pop('departments', [])
        
        # Create administrator instance
        administrator = Administrator.objects.create(**validated_data)
        
        # Add departments explicitly
        if departments_data:
            administrator.departments.set(departments_data)
            administrator.save()
        
        return administrator

    def update(self, instance, validated_data):
        # Extract departments from validated data
        departments_data = validated_data.pop('departments', None)
        
        # Update administrator fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update departments if provided
        if departments_data is not None:
            instance.departments.set(departments_data)
        
        instance.save()
        return instance

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)
        
        # Add department IDs to verify they're being saved
        representation['department_ids'] = list(instance.departments.values_list('department_id', flat=True))
        
        return representation