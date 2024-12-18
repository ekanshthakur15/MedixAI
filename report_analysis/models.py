import datetime

from django.contrib.auth.models import User
from django.db import models


class Treatment(models.Model):
    name = models.CharField(max_length= 100)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self) -> str:
        return self.name
# Create your models here.
class MedicalReport(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,null= True, blank= True)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE , blank= True, null= True)
    name = models.CharField(max_length=150)
    test_date = models.DateField(default=datetime.date.today())

    report = models.FileField(upload_to= "medical_reports/")

    def __str__(self) -> str:
        return self.name

class ReportAttributes(models.Model):

    medical_report = models.ForeignKey(MedicalReport, on_delete=models.CASCADE)
    element = models.CharField(max_length=100)
    unit = models.CharField(max_length=50,blank=True, null=True)
    reference_low = models.CharField(max_length=50,blank=True, null=True)
    reference_high = models.CharField(max_length=50,blank=True, null=True)
    result = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.element + self.medical_report.name
    
class ReportSummary(models.Model):
    medical_report = models.ForeignKey(MedicalReport, on_delete=models.CASCADE)
    summary = models.TextField(null=True , blank= True)

    def __str__(self) -> str:
        return self.medical_report.name