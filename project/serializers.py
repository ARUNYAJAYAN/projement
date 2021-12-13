from rest_framework import serializers
from project.models import Project, Tag, Log


class ProjectSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data.get("actual_design") > 10000.00:
            raise serializers.ValidationError({"actual_design": "Maximum 10000 allowed"})
        if data.get("actual_development") > 10000.00:
            raise serializers.ValidationError({"actual_development": "Maximum 10000 allowed"})
        if data.get("actual_testing") > 10000.00:
            raise serializers.ValidationError({"actual_testing": "Maximum 10000 allowed"})
        if 'additional_development' in data:
            data['additional_development'] = self.instance.additional_development + data['additional_development']
        return data

    class Meta:
        model = Project
        fields = '__all__'


class ProjectListSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    total_estimated_hours = serializers.SerializerMethodField()
    total_actual_hours = serializers.SerializerMethodField()

    def get_company(self, obj):
        if obj.company:
            return {
                "id": obj.company.id,
                "name": obj.company.name
            }
        return {}

    def get_total_estimated_hours(self, obj):
        return obj.total_estimated_hours

    def get_total_actual_hours(self, obj):
        return obj.total_actual_hours

    class Meta:
        model = Project
        read_only_fields = ['company', 'total_estimated_hours', 'total_actual_hours']
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class TagListSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()

    def get_project(self, obj):
        if obj.project:
            return {
                "id": obj.project.id,
                "name": obj.project.title
            }
        return {}

    class Meta:
        model = Tag
        read_only_fields = ['project']
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    developer = serializers.SerializerMethodField()

    def get_developer(self, obj):
        if obj.developer:
            return {
                "id": obj.developer.id,
                "name": obj.developer.name
            }
        return {}

    class Meta:
        model = Log
        read_only_fields = ['developer']
        fields = '__all__'