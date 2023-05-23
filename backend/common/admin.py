from django.contrib import admin

# Register your models here.
from .models import Applicant, Job

admin.site.register(Applicant)
admin.site.register(Job)
