from django.contrib import admin

from project.models import Project, Tag, Log

admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Log)
# Register your models here.
