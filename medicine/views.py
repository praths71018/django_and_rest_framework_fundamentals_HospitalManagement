from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Medicine
from .serializers import MedicineSerializer
from django.core.cache import cache
import time # for caching time

class MedicineListView(APIView):
    def get(self, request):
        cache_data = cache.get('all_medicines') # all_medicines is the key for the cache
        if cache_data: # 1st time request will be slow as taking from db, so we will cache the data and return the cached data
            return Response(cache_data) # if cache_data is not None, return the cache_data
        medicines = Medicine.objects.all()
        serializer = MedicineSerializer(medicines, many=True)
        cache.set('all_medicines', serializer.data, timeout=60*60) # cache the data for 1 hour
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicineDetailView(APIView):
    def get_object(self, medicine_id):
        try:
            return Medicine.objects.get(medicine_id=medicine_id)
        except Medicine.DoesNotExist:
            return None

    def get(self, request, medicine_id):
        medicine = self.get_object(medicine_id)
        if not medicine:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data)

    def put(self, request, medicine_id):
        medicine = self.get_object(medicine_id)
        if not medicine:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = MedicineSerializer(medicine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, medicine_id):
        medicine = self.get_object(medicine_id)
        if not medicine:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        medicine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Medicine
# from .serializers import MedicineSerializer

# @api_view(['GET', 'POST'])
# def medicine_list(request):
#     if request.method == 'GET':
#         medicines = Medicine.objects.all()
#         serializer = MedicineSerializer(medicines, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = MedicineSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def medicine_detail(request, medicine_id):
#     try:
#         medicine = Medicine.objects.get(medicine_id=medicine_id)
#     except Medicine.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = MedicineSerializer(medicine)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = MedicineSerializer(medicine, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         medicine.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


