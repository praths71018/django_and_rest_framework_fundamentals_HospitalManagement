from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from .models import LoginHistory
import os

# Set up the Login_History log file path
login_history_file_path = os.path.join('logs', 'Login_History.log')  # Ensure the 'logs' directory exists
os.makedirs(os.path.dirname(login_history_file_path), exist_ok=True)

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = get_object_or_404(User, username=username)

        # Capture the IP address
        ip_address = request.META.get('REMOTE_ADDR')

        if not user.check_password(password):
            # Log failed login attempt
            login_history = LoginHistory.objects.create(
                user=user,
                success=False,
                ip_address=ip_address
            )
            # Save the LoginHistory object contents to the log
            with open(login_history_file_path, 'a') as log_file:
                log_file.write(f"{login_history.user.username} - {login_history.timestamp} - Failure - {login_history.ip_address}\n")
            return Response("Invalid credentials", status=status.HTTP_404_NOT_FOUND)

        # Log successful login attempt
        token, created = Token.objects.get_or_create(user=user)
        login_history = LoginHistory.objects.create(
            user=user,
            success=True,
            ip_address=ip_address
        )
        # Save the LoginHistory object contents to the log
        with open(login_history_file_path, 'a') as log_file:
            log_file.write(f"{login_history.user.username} - {login_history.timestamp} - Success - {login_history.ip_address}\n")
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})

class TestTokenView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response("passed!")