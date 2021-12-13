from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework import generics
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework import authentication, permissions
from itertools import chain
from utils.decorators import allowed_users
from utils.export import export_project_data

from project.serializers import ProjectSerializer, ProjectListSerializer, TagSerializer, TagListSerializer, \
    LogSerializer
from project.models import Project, Tag, Log
from developer.models import Developer


class ProjectCreate(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def create(self, request):
        allowed_users(allowed_roles=['admin'])
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors,
                             "message": "Something went wrong"})
        else:
            serializer.save()
            return Response({"status": status.HTTP_201_CREATED, "data": serializer.data, "message": "Your details saved successfully"})

    @method_decorator(allowed_users(allowed_roles=['admin', 'developer']))
    def list(self, request):
        # allowed_users(request, allowed_roles=['anoop'])
        first_queryset = self.queryset.filter(end_date__gt=timezone.now().date())
        second_queryset = Project.objects.all().order_by('-end_date')
        combined_queryset = list(chain(first_queryset, second_queryset))
        serializer = ProjectListSerializer(combined_queryset, many=True)
        data = [i for n, i in enumerate(serializer.data) if i not in serializer.data[n + 1:]]
        return Response({"status": status.HTTP_200_OK, "data": data, "message": "Project list"})


class ProjectUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(allowed_users(allowed_roles=['admin', 'developer']))
    def update(self, request, pk, *args, **kwargs):
        old_data = Project.objects.filter(id=pk).first()
        serializer = self.get_serializer(data=request.data, instance=self.get_object())

        if not serializer.is_valid():
            return Response({"status": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors, "message": "Something went wrong"})
        else:
            serializer.save()
            old_data = ProjectSerializer(old_data, many=False).data
            new_data = serializer.data
            if Developer.objects.filter(id=request.user.id).first():
                log = Log()
                log.old_estimate = old_data
                log.new_estimate = new_data
                log.developer = Developer.objects.filter(id=request.user.id).first()
                log.save()
            return Response({"status": status.HTTP_200_OK, "data": serializer.data, "message": "Your details saved successfully"})

    @method_decorator(allowed_users(allowed_roles=['admin', 'developer']))
    def retrieve(self, request, *args, **kwargs):
        serializer = ProjectSerializer(self.get_object(), many=False)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data, "message": "Project Detail"})

    @method_decorator(allowed_users(allowed_roles=['admin', 'developer']))
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "errors": {}, "message": "Something went wrong"})
        self.perform_destroy(instance)
        return Response({"status": status.HTTP_200_OK, "data": {}, "message": "Deleted successfully"})


class ListCompanyProjects(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def list(self, request, company_id, *args, **kwargs):
        queryset = Project.objects.filter(company=company_id).order_by('-end_date')
        serializer = ProjectListSerializer(queryset, many=True)
        data = [i for n, i in enumerate(serializer.data) if i not in serializer.data[n + 1:]]
        return Response({"status": status.HTTP_200_OK, "data": data, "message": "Project list"})


class TagCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

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
        serializer = TagListSerializer(self.get_queryset(), many=True)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data, "message": "Project's tag list"})


class TagUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, instance=self.get_object())

        if not serializer.is_valid():
            return Response({"status": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors, "message": "Something went wrong"})
        else:
            serializer.save()
            return Response({"status": status.HTTP_200_OK, "data": serializer.data, "message": "Your details saved successfully"})

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def retrieve(self, request, *args, **kwargs):
        serializer = TagListSerializer(self.get_object(), many=False)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data, "message": "Tag's Detail"})

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "errors": {}, "message": "Something went wrong"})
        self.perform_destroy(instance)
        return Response({"status": status.HTTP_201_CREATED, "data": {}, "message": "Deleted successfully"})


class ProjectFile(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def list(self, request):
        queryset = Project.objects.all()
        serializer = ProjectListSerializer(queryset, many=True)
        db_data = list(serializer.data)
        data = []
        for i in db_data:
            data_dict = {}
            data_dict['Project'] = i['title']
            data_dict['Company'] = i['company']['name']
            data_dict['Estimated'] = i['total_estimated_hours']
            data_dict['Actual'] = i['total_actual_hours']
            data_dict['Additional development'] = i['additional_development']
            data.append(data_dict)
        export_project_data(data)
        short_report = open("project.xls", 'rb').read()
        filename = "project.xls"
        response = HttpResponse(short_report)
        response.headers['Content-Type'] = 'application/vnd.ms-excel;charset=UTF-8'
        response.headers['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response


class LogList(generics.ListAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def list(self, request):
        serializer = LogSerializer(self.get_queryset(), many=True)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data, "message": "Log's list"})

