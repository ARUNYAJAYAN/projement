from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.utils.decorators import method_decorator
from rest_framework import status
from developer.models import Developer
from developer.serializers import DeveloperSerializer
from utils.decorators import allowed_users


class DeveloperList(generics.ListCreateAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors, "message": "Something went wrong"})
        else:
            serializer.save()
            return Response({"status": status.HTTP_201_CREATED, "data": serializer.data, "message": "Your details saved successfully"})

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response({"status": status.HTTP_200_OK, "data": serializer.data, "message": "Developers list"})


class DeveloperDetail(generics.RetrieveAPIView):
    queryset = Developer
    serializer_class = DeveloperSerializer
    @method_decorator(allowed_users(allowed_roles=['admin', 'developer']))
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), many=False)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data, "message": "Developer's Detail"})
