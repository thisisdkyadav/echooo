from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *
from django.contrib.auth.models import User


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Data received', 'data': serializer.data})
        
        return Response({'message': 'error' , 'error': serializer.errors})
    

