from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from utils.decorators import allowed_users
from company.models import Company
from company.serializers import CompanySerializer
from rest_framework import authentication, permissions
from utils.decorators import allowed_users


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(allowed_users(allowed_roles=['admin', 'management']))
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors, "message": "Something went wrong"})
        else:
            serializer.save()
            return Response({"status": status.HTTP_201_CREATED, "data": serializer.data, "message": "Your details saved successfully"})

    @method_decorator(allowed_users(allowed_roles=['admin', 'Developer', 'management']))
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response({"status": status.HTTP_200_OK, "data": serializer.data, "message": "Companies list"})


class CompanyDetail(generics.RetrieveAPIView):
    queryset = Company
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(allowed_users(allowed_roles=['admin', 'Developer', 'management']))
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), many=False)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data, "message": "Company's Detail"})
