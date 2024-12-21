from django.shortcuts import render
from rest_framework import status, permissions, generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserUpdateSerializer, UserGroupAssignmentSerializer
from .models import User
from django.contrib.auth.models import Group


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserGroupAssignmentView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserGroupAssignmentSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can assign groups

    def get_object(self):
        return self.request.user  # Update the authenticated user
