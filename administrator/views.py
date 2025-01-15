from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Administrator, Hospital, Department
from .serializers import AdministratorSerializer, HospitalSerializer, DepartmentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Administrator, Hospital, Department
from .serializers import AdministratorSerializer, HospitalSerializer, DepartmentSerializer
from rest_framework.permissions import IsAuthenticated

class AdministratorListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        administrators = Administrator.objects.all()
        serializer = AdministratorSerializer(administrators, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            # Print request data for debugging
            print("Received POST data:", request.data)
            
            # Ensure hospital_id is provided
            if 'hospital' not in request.data:
                return Response(
                    {"error": "hospital field is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Ensure departments are provided
            if 'departments' not in request.data:
                return Response(
                    {"error": "departments field is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate if the hospital exists
            try:
                Hospital.objects.get(Hospital_id=request.data['hospital'])
            except Hospital.DoesNotExist:
                return Response(
                    {"error": f"Hospital with id {request.data['hospital']} does not exist"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate departments exist
            department_ids = request.data.get('departments', [])
            existing_departments = Department.objects.filter(department_id__in=department_ids)
            if len(existing_departments) != len(department_ids):
                return Response(
                    {"error": "One or more department IDs are invalid"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = AdministratorSerializer(data=request.data)
            if serializer.is_valid():
                administrator = serializer.save()
                # Verify departments were saved
                print("Saved departments:", list(administrator.departments.all()))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print("Error creating administrator:", str(e))
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class AdministratorDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, admin_id):
        try:
            return Administrator.objects.get(admin_id=admin_id)
        except Administrator.DoesNotExist:
            return None

    def get(self, request, admin_id):
        admin = self.get_object(admin_id)
        if not admin:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = AdministratorSerializer(admin)
        return Response(serializer.data)

    def put(self, request, admin_id):
        admin = self.get_object(admin_id)
        if not admin:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = AdministratorSerializer(admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, admin_id):
        admin = self.get_object(admin_id)
        if not admin:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HospitalDetailView(APIView):
    def get(self, request, hospital_id):
        try:
            hospital = Hospital.objects.get(Hospital_id=hospital_id)
            serializer = HospitalSerializer(hospital)
            return Response(serializer.data)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DepartmentDetailView(APIView):
    def get(self, request, dept_id):
        try:
            department = Department.objects.get(department_id=dept_id)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET', 'POST'])
# def administrator_list(request):
#     if request.method == 'GET':
#         administrators = Administrator.objects.all()
#         serializer = AdministratorSerializer(administrators, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         try:
#             # Print request data for debugging
#             print("Received POST data:", request.data)
            
#             # Ensure hospital_id is provided
#             if 'hospital' not in request.data:
#                 return Response(
#                     {"error": "hospital field is required"}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             # Ensure departments are provided
#             if 'departments' not in request.data:
#                 return Response(
#                     {"error": "departments field is required"}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             # Validate if the hospital exists
#             try:
#                 Hospital.objects.get(Hospital_id=request.data['hospital'])
#             except Hospital.DoesNotExist:
#                 return Response(
#                     {"error": f"Hospital with id {request.data['hospital']} does not exist"}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Validate departments exist
#             department_ids = request.data.get('departments', [])
#             existing_departments = Department.objects.filter(department_id__in=department_ids)
#             if len(existing_departments) != len(department_ids):
#                 return Response(
#                     {"error": "One or more department IDs are invalid"}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             serializer = AdministratorSerializer(data=request.data)
#             if serializer.is_valid():
#                 administrator = serializer.save()
#                 # Verify departments were saved
#                 print("Saved departments:", list(administrator.departments.all()))
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#         except Exception as e:
#             print("Error creating administrator:", str(e))
#             return Response(
#                 {"error": str(e)}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )

# @api_view(['GET', 'PUT', 'DELETE'])
# def administrator_detail(request, admin_id):
#     try:
#         admin = Administrator.objects.get(admin_id=admin_id)
#     except Administrator.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = AdministratorSerializer(admin)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = AdministratorSerializer(admin, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         admin.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# def hospital_detail(request, hospital_id):
#     try:
#         hospital = Hospital.objects.get(Hospital_id=hospital_id)
#     except Hospital.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = HospitalSerializer(hospital)
#         return Response(serializer.data)

# @api_view(['GET'])
# def department_detail(request, dept_id):
#     try:
#         department = Department.objects.get(department_id=dept_id)
#     except Department.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = DepartmentSerializer(department)
#         return Response(serializer.data)
