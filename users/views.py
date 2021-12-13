from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from users.serializers import RegistrationSerializer, LoginSerializer
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.models import Token
from developer.models import Developer


class RegisterUser(APIView):
    """
    API For Register User
    """

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if 2 in request.data['groups']:
                developer = Developer()
                developer.name = request.data['first_name'] + " " + request.data['last_name']
                developer.save(self)
            if user:
                user.set_password(request.data.get("password"))
                token = Token.objects.create(user=user)
                user.save()
                json = serializer.data
                json['token'] = token.key
                return Response({"status": status.HTTP_201_CREATED, "data": json,
                                 "message": "Your details saved successfully"})
        return Response({"status": status.HTTP_400_BAD_REQUEST, "errors": {serializer.errors},
                         "message": "Something went wrong"})


class LoginUser(APIView):
    """
    API For Login User
    """

    def post(self, request, format='json'):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({"status": status.HTTP_200_OK,
                                 "data": {"token": Token.objects.get_or_create(user=user)[0].key},
                                 "message": "Login success"})
            return Response({"status": status.HTTP_400_BAD_REQUEST, "errors": {serializer.errors},
                             "message": "Something went wrong"})


class Logout(APIView):
    """
    API For Logging out user
    """

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response({"status": status.HTTP_200_OK, "data": {"Logout": "Logged out successfully"},
                         "message": "Something went wrong"})