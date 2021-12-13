from django.db import models
from django.utils import timezone


# Create company model
class Company(models.Model):
    name = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)