from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Disease
from .serializers import DiseaseSerializer

class DiseaseListView(APIView):
    def get(self, request):
        diseases = Disease.objects.all()
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiseaseDetailView(APIView):
    def get_object(self, disease_id):
        try:
            return Disease.objects.get(disease_id=disease_id)
        except Disease.DoesNotExist:
            return None

    def get(self, request, disease_id):
        disease = self.get_object(disease_id)
        if not disease:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = DiseaseSerializer(disease)
        return Response(serializer.data)

    def put(self, request, disease_id):
        disease = self.get_object(disease_id)
        if not disease:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = DiseaseSerializer(disease, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, disease_id):
        disease = self.get_object(disease_id)
        if not disease:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        disease.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Disease
# from .serializers import DiseaseSerializer

# @api_view(['GET', 'POST'])
# def disease_list(request):
#     if request.method == 'GET':
#         diseases = Disease.objects.all()
#         serializer = DiseaseSerializer(diseases, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = DiseaseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def disease_detail(request, disease_id):
#     try:
#         disease = Disease.objects.get(disease_id=disease_id)
#     except Disease.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = DiseaseSerializer(disease)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = DiseaseSerializer(disease, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         disease.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


