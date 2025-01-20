from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile, CSVParser
from .serializers import UserProfileSerializer
import csv
import os
from django.conf import settings
from django.contrib.auth.models import User

# Create your views here.

class UserProfileList(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

class CSVDataView(APIView):
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'csv_parser', 'data.csv')
        
        # Ensure the CSV file exists before reading
        if not os.path.exists(file_path):
            return Response({"error": "CSV file does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        data = CSVParser.read_csv(file_path)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # Get the JSON data from the request
        json_data = request.data
        print(json_data)
        
        # Check if the incoming data is a dictionary
        if not isinstance(json_data, dict):
            return Response({"error": "Invalid data format. Expected a single user profile."}, status=status.HTTP_400_BAD_REQUEST)

        user_id = json_data.get('user_id')
        father_name = json_data.get('father_name')
        
        # Check if user_id and father_name are provided
        if user_id is None or father_name is None:
            return Response({"error": "Both user_id and father_name must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming you have a User model and you can get the user by ID
        try:
            user = User.objects.get(id=user_id)
            username = user.username  # Retrieve the username
            UserProfile.objects.update_or_create(user=user, defaults={'father_name': father_name})
            response_data = {'user_id': user_id, 'username': username, 'father_name': father_name}  # Prepare response data
        except User.DoesNotExist:
            return Response({"error": f"User with ID {user_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Write updated data back to the CSV file
        file_path = os.path.join(settings.BASE_DIR, 'csv_parser', 'data.csv')
        with open(file_path, mode='a', newline='') as file:  # Append mode
            writer = csv.DictWriter(file, fieldnames=['user_id', 'username', 'father_name'])
            writer.writerow({'user_id': user_id, 'username': username, 'father_name': father_name})  # Write the new row

        return Response({"message": "User profile updated successfully.", "data": response_data}, status=status.HTTP_201_CREATED)
