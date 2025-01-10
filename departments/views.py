from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Department
from .serializers import DepartmentSerializer

class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentDetailView(APIView):
    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return None

    def get(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Department
# from .serializers import DepartmentSerializer

# @api_view(['GET', 'POST'])
# def department_list(request):
#     if request.method == 'GET':
#         departments = Department.objects.all()
#         serializer = DepartmentSerializer(departments, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = DepartmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def department_detail(request, pk):
#     try:
#         department = Department.objects.get(pk=pk)
#     except Department.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = DepartmentSerializer(department)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = DepartmentSerializer(department, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         department.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
