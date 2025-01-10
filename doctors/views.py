from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .serializers import DoctorSerializer
from administrator.models import Administrator

class DoctorListView(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            # Check if department exists under administrator's hospital
            hospital_id = request.data.get('hospital_id')
            department_id = request.data.get('department_id')
            
            try:
                # Check if any administrator of this hospital manages this department
                administrator = Administrator.objects.filter(
                    hospital_id=hospital_id,
                    departments__department_id=department_id
                ).first()
                
                if not administrator:
                    return Response(
                        {"error": "This department is not managed by any administrator in this hospital"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorDetailView(APIView):
    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return None

    def get(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            # Check if department exists under administrator's hospital
            hospital_id = request.data.get('hospital_id')
            department_id = request.data.get('department_id')
            
            try:
                # Check if any administrator of this hospital manages this department
                administrator = Administrator.objects.filter(
                    hospital_id=hospital_id,
                    departments__department_id=department_id
                ).first()
                
                if not administrator:
                    return Response(
                        {"error": "This department is not managed by any administrator in this hospital"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
                serializer.save()
                return Response(serializer.data)
                
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Doctor
# from .serializers import DoctorSerializer
# from administrator.models import Administrator

# @api_view(['GET', 'POST'])
# def doctor_list(request):
#     if request.method == 'GET':
#         doctors = Doctor.objects.all()
#         serializer = DoctorSerializer(doctors, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = DoctorSerializer(data=request.data)
#         if serializer.is_valid():
#             # Check if department exists under administrator's hospital
#             hospital_id = request.data.get('hospital_id')
#             department_id = request.data.get('department_id')
            
#             try:
#                 # Check if any administrator of this hospital manages this department
#                 administrator = Administrator.objects.filter(
#                     hospital_id=hospital_id,
#                     departments__department_id=department_id
#                 ).first()
                
#                 if not administrator:
#                     return Response(
#                         {"error": "This department is not managed by any administrator in this hospital"},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
                    
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
                
#             except Exception as e:
#                 return Response(
#                     {"error": str(e)},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
                
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT', 'DELETE'])
# def doctor_detail(request, pk):
#     try:
#         doctor = Doctor.objects.get(pk=pk)
#     except Doctor.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = DoctorSerializer(doctor, data=request.data)
#         if serializer.is_valid():
#             # Check if department exists under administrator's hospital
#             hospital_id = request.data.get('hospital_id')
#             department_id = request.data.get('department_id')
            
#             try:
#                 # Check if any administrator of this hospital manages this department
#                 administrator = Administrator.objects.filter(
#                     hospital_id=hospital_id,
#                     departments__department_id=department_id
#                 ).first()
                
#                 if not administrator:
#                     return Response(
#                         {"error": "This department is not managed by any administrator in this hospital"},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
                    
#                 serializer.save()
#                 return Response(serializer.data)
                
#             except Exception as e:
#                 return Response(
#                     {"error": str(e)},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
                
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         doctor.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
