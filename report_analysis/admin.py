from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(MedicalReport)
admin.site.register(ReportAttributes)
admin.site.register(ReportSummary)
