from django.db import models
from company.models import Company
from developer.models import Developer
from django.utils import timezone
from jsonfield import JSONField


# Create project model here.
class Project(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    estimated_design = models.IntegerField(default=0)
    actual_design = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    estimated_development = models.IntegerField(default=0)
    actual_development = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    estimated_testing = models.IntegerField(default=0)
    actual_testing = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    additional_development = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def has_ended(self):
        return self.end_date is not None and self.end_date < timezone.now().date()

    @property
    def total_estimated_hours(self):
        return self.estimated_design + self.estimated_development + self.estimated_testing

    @property
    def total_actual_hours(self):
        return self.actual_design + self.actual_development + self.actual_testing

    @property
    def is_over_budget(self):
        return self.total_actual_hours > self.total_estimated_hours


# Create Tag model
class Tag(models.Model):
    name = models.CharField(max_length=16)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)


# Create Log model
class Log(models.Model):
    old_estimate = JSONField()
    new_estimate = JSONField()
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)