from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hospital
from .serializers import HospitalSerializer

class HospitalListView(APIView):
    def get(self, request):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HospitalDetailView(APIView):
    def get_object(self, pk):
        try:
            return Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            return None

    def get(self, request, pk):
        hospital = self.get_object(pk)
        if not hospital:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = HospitalSerializer(hospital)
        return Response(serializer.data)

    def put(self, request, pk):
        hospital = self.get_object(pk)
        if not hospital:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = HospitalSerializer(hospital, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        hospital = self.get_object(pk)
        if not hospital:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        hospital.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Hospital
# from .serializers import HospitalSerializer

# @api_view(['GET', 'POST'])
# def hospital_list(request):
#     if request.method == 'GET':
#         hospitals = Hospital.objects.all()
#         serializer = HospitalSerializer(hospitals, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = HospitalSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def hospital_detail(request, pk):
#     try:
#         hospital = Hospital.objects.get(pk=pk)
#     except Hospital.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = HospitalSerializer(hospital)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = HospitalSerializer(hospital, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         hospital.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
